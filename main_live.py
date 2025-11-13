"""
Main entry point for live trading system
Runs AI agent with real-time market data and trade execution
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from tools.general_tools import write_config_value
from agent_tools.providers import AlpacaDataProvider, BinanceDataProvider
from risk_management import RiskManager


async def main_live(config_path: str = "configs/live_config.json"):
    """
    Main function for live trading

    Args:
        config_path: Path to live trading configuration file
    """
    print("=" * 80)
    print("AI-Trader Live Trading System")
    print("=" * 80)

    # Load configuration
    with open(config_path, "r") as f:
        config = json.load(f)

    print(f"\n📋 Configuration loaded from: {config_path}")
    print(f"🤖 Model: {config['model']['name']}")
    print(f"💼 Broker: {config['broker_type']}")
    print(f"🎯 Trading Mode: {config['trading_mode']}")

    # Confirm before proceeding
    if config["trading_mode"] == "live":
        print("\n⚠️  WARNING: LIVE TRADING MODE - REAL MONEY WILL BE USED!")
        confirmation = input("Type 'YES' to continue with live trading: ")
        if confirmation != "YES":
            print("Aborted.")
            return

    # Set configuration in environment
    write_config_value("BROKER_TYPE", config["broker_type"])
    write_config_value("TRADING_MODE", config["trading_mode"])
    write_config_value("LIVE_CONFIG_PATH", config_path)

    # Initialize risk manager
    log_path = Path(config.get("log_path", "data/live_logs"))
    risk_manager = RiskManager(config, log_path=log_path / "risk_logs")
    print(f"\n✅ Risk manager initialized")
    print(f"📊 Risk stats: {risk_manager.get_stats()}")

    # Initialize MCP client with live trading tools
    print("\n🔌 Connecting to MCP services...")

    mcp_servers = {
        "live_trading": {
            "command": "python",
            "args": [
                str(Path(project_root) / "agent_tools" / "tool_trade_live.py")
            ],
        },
        "live_prices": {
            "command": "python",
            "args": [
                str(Path(project_root) / "agent_tools" / "tool_get_price_live.py")
            ],
        },
        "search": {
            "command": "python",
            "args": [
                str(Path(project_root) / "agent_tools" / "tool_jina_search.py")
            ],
        },
    }

    async with MultiServerMCPClient(mcp_servers) as client:
        tools = await client.list_tools()
        print(f"\n✅ Connected to MCP services")
        print(f"🔧 Available tools: {len(tools)}")
        for tool in tools:
            print(f"   - {tool.name}")

        # Initialize AI model
        model_config = config["model"]
        print(f"\n🤖 Initializing AI model: {model_config['name']}")

        llm = ChatOpenAI(
            model=model_config["basemodel"],
            temperature=0.7,
            base_url=os.getenv("OPENAI_API_BASE"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Bind tools to model
        llm_with_tools = llm.bind_tools(tools)

        # Get initial account status
        print("\n💰 Getting account status...")
        # We'll invoke the tool directly through MCP
        account_result = await client.call_tool(
            "live_trading",
            "get_account_status",
            {}
        )
        print(f"📊 Account: {json.dumps(account_result, indent=2)}")

        # Create trading system prompt
        system_prompt = f"""You are an AI trading agent managing a real trading account.

Current Date/Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Account Status:
{json.dumps(account_result, indent=2)}

Your role:
1. Analyze market conditions using available tools
2. Make trading decisions based on analysis
3. Execute trades using buy_live() and sell_live() tools
4. Monitor positions and risk

Available tools:
- get_price_live(symbol): Get current real-time price
- buy_live(symbol, amount): Place buy order
- sell_live(symbol, amount): Place sell order
- get_account_status(): Get current account info
- get_information(query): Search for market news/info
- emergency_stop(reason): Halt all trading

Risk Management:
- All trades go through automated risk checks
- Daily trade limit: {config.get('risk_controls', {}).get('max_daily_trades', 50)}
- Max single trade: {config.get('risk_controls', {}).get('max_single_trade_pct', 0.10)*100}%
- Max position: {config.get('risk_controls', {}).get('max_position_pct', 0.30)*100}%

Trading Guidelines:
1. Start with market research before trading
2. Diversify positions across multiple symbols
3. Set clear entry and exit strategies
4. Monitor for stop-loss triggers
5. Trade conservatively and manage risk

⚠️ IMPORTANT: This is {config['trading_mode']} trading mode!
"""

        # Trading loop
        print("\n🚀 Starting live trading agent...")
        print("=" * 80)

        iteration = 0
        max_iterations = config.get("max_iterations", 100)

        while iteration < max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")

            try:
                # Get AI decision
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Analyze the market and make trading decisions."}
                ]

                response = await llm_with_tools.ainvoke(messages)

                # Check for tool calls
                if hasattr(response, "tool_calls") and response.tool_calls:
                    print(f"🔧 AI requested {len(response.tool_calls)} tool calls")

                    for tool_call in response.tool_calls:
                        tool_name = tool_call["name"]
                        tool_args = tool_call["args"]

                        print(f"   📞 Calling: {tool_name}({tool_args})")

                        # Execute tool through MCP
                        # Determine which server has this tool
                        if tool_name in ["buy_live", "sell_live", "get_account_status", "emergency_stop"]:
                            server = "live_trading"
                        elif tool_name in ["get_price_live", "get_price_historical", "get_multiple_prices"]:
                            server = "live_prices"
                        elif tool_name in ["get_information"]:
                            server = "search"
                        else:
                            print(f"   ❌ Unknown tool: {tool_name}")
                            continue

                        result = await client.call_tool(server, tool_name, tool_args)
                        print(f"   ✅ Result: {json.dumps(result, indent=6)}")

                else:
                    # No tool calls, just text response
                    print(f"💭 AI response: {response.content}")

                # Wait before next iteration
                wait_time = config.get("iteration_wait_seconds", 60)
                print(f"\n⏳ Waiting {wait_time} seconds before next iteration...")
                await asyncio.sleep(wait_time)

            except KeyboardInterrupt:
                print("\n\n🛑 Interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Error in iteration {iteration}: {e}")
                import traceback
                traceback.print_exc()

                # Wait before retrying
                await asyncio.sleep(10)

        print("\n" + "=" * 80)
        print("Live trading session ended")
        print("=" * 80)


if __name__ == "__main__":
    # Get config path from command line or use default
    config_path = sys.argv[1] if len(sys.argv) > 1 else "configs/live_config.json"

    # Run main
    asyncio.run(main_live(config_path))
