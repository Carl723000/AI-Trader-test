"""
Live Trading Tool - MCP tool for real-time trade execution
Integrates with brokers and risk management system
"""

import os
import sys
import json
from pathlib import Path
from typing import Any, Dict, Optional

from fastmcp import FastMCP
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tools.general_tools import get_config_value
from agent_tools.brokers import BaseBroker, AlpacaBroker, BinanceBroker, OrderSide, OrderType
from agent_tools.providers import MarketDataProvider, AlpacaDataProvider, BinanceDataProvider
from risk_management import RiskManager

load_dotenv()

mcp = FastMCP("LiveTrading")

# Global instances (initialized when needed)
_broker: Optional[BaseBroker] = None
_provider: Optional[MarketDataProvider] = None
_risk_manager: Optional[RiskManager] = None


async def _get_broker() -> BaseBroker:
    """Get or create broker instance"""
    global _broker

    if _broker is None:
        broker_type = get_config_value("BROKER_TYPE") or "alpaca"
        trading_mode = get_config_value("TRADING_MODE") or "paper"

        if broker_type == "alpaca":
            api_key = os.getenv("ALPACA_API_KEY")
            api_secret = os.getenv("ALPACA_API_SECRET")

            if trading_mode == "live":
                base_url = "https://api.alpaca.markets"
            else:
                base_url = "https://paper-api.alpaca.markets"

            _broker = AlpacaBroker(api_key, api_secret, base_url=base_url)

        elif broker_type == "binance":
            api_key = os.getenv("BINANCE_API_KEY")
            api_secret = os.getenv("BINANCE_API_SECRET")
            testnet = trading_mode == "paper"

            _broker = BinanceBroker(api_key, api_secret, testnet=testnet)

        else:
            raise ValueError(f"Unsupported broker type: {broker_type}")

        # Connect to broker
        connected = await _broker.connect()
        if not connected:
            raise ConnectionError(f"Failed to connect to {broker_type} broker")

        print(f"✅ Connected to {broker_type} broker ({trading_mode} mode)")

    return _broker


async def _get_provider() -> MarketDataProvider:
    """Get or create market data provider"""
    global _provider

    if _provider is None:
        broker_type = get_config_value("BROKER_TYPE") or "alpaca"
        trading_mode = get_config_value("TRADING_MODE") or "paper"

        if broker_type == "alpaca":
            api_key = os.getenv("ALPACA_API_KEY")
            api_secret = os.getenv("ALPACA_API_SECRET")

            if trading_mode == "live":
                base_url = "https://api.alpaca.markets"
            else:
                base_url = "https://paper-api.alpaca.markets"

            _provider = AlpacaDataProvider(api_key, api_secret, base_url=base_url)

        elif broker_type == "binance":
            api_key = os.getenv("BINANCE_API_KEY")
            api_secret = os.getenv("BINANCE_API_SECRET")
            testnet = trading_mode == "paper"

            _provider = BinanceDataProvider(api_key, api_secret, testnet=testnet)

        else:
            raise ValueError(f"Unsupported provider type: {broker_type}")

        # Connect to provider
        connected = await _provider.connect()
        if not connected:
            raise ConnectionError(f"Failed to connect to {broker_type} data provider")

        print(f"✅ Connected to {broker_type} data provider")

    return _provider


async def _get_risk_manager() -> RiskManager:
    """Get or create risk manager"""
    global _risk_manager

    if _risk_manager is None:
        # Load risk configuration
        config_path = get_config_value("LIVE_CONFIG_PATH")
        if config_path and Path(config_path).exists():
            with open(config_path, "r") as f:
                config = json.load(f)
        else:
            # Default risk configuration
            config = {
                "risk_controls": {
                    "max_single_trade_pct": 0.10,
                    "max_position_pct": 0.30,
                    "max_daily_trades": 50,
                    "max_daily_loss_pct": 0.05,
                    "enable_emergency_stop": True,
                }
            }

        log_path = Path(project_root) / "data" / "risk_logs"
        _risk_manager = RiskManager(config, log_path=log_path)

        print(f"✅ Risk manager initialized")

    return _risk_manager


@mcp.tool()
async def buy_live(symbol: str, amount: int) -> Dict[str, Any]:
    """
    Place a live buy order for stocks or cryptocurrency

    This function executes a REAL trade on connected brokerage account.
    It includes risk management checks before execution.

    ⚠️ WARNING: This will use real money in live trading mode!

    Args:
        symbol: Stock/crypto symbol (e.g., "AAPL", "BTCUSDT")
        amount: Quantity to buy (must be positive integer)

    Returns:
        Dict containing:
        - success: Whether order was placed
        - order_id: Broker's order ID
        - message: Status message
        - order_details: Full order information

    Example:
        >>> result = await buy_live("AAPL", 10)
        >>> print(result)  # {"success": True, "order_id": "...", ...}
    """
    try:
        # Get instances
        broker = await _get_broker()
        provider = await _get_provider()
        risk_manager = await _get_risk_manager()

        # Validate amount
        try:
            amount = int(amount)
            if amount <= 0:
                return {"success": False, "error": "Amount must be positive"}
        except ValueError:
            return {"success": False, "error": "Amount must be an integer"}

        # Get current price
        price_data = await provider.get_realtime_price(symbol)
        if not price_data:
            return {"success": False, "error": f"Could not get price for {symbol}"}

        price = price_data.buy_price or price_data.close

        # Get account info
        account_info = await provider.get_account_info()
        if not account_info:
            return {"success": False, "error": "Could not get account information"}

        # Risk check
        risk_result = await risk_manager.check_trade(
            symbol=symbol,
            side="buy",
            quantity=amount,
            price=price,
            account_info=account_info.to_dict()
        )

        if not risk_result.approved:
            violations_str = "\n".join([
                f"- {v.message}" for v in risk_result.violations
            ])
            return {
                "success": False,
                "error": "Risk check failed",
                "violations": violations_str,
                "risk_details": risk_result.to_dict()
            }

        # Place order
        order = await broker.place_order(
            symbol=symbol,
            side=OrderSide.BUY,
            quantity=amount,
            order_type=OrderType.MARKET
        )

        if not order:
            return {"success": False, "error": "Order placement failed"}

        # Increment trade counter
        risk_manager.increment_trade_count()

        return {
            "success": True,
            "order_id": order.order_id,
            "message": f"Buy order placed: {amount} {symbol} @ ${price:.2f}",
            "order_details": order.to_dict()
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Exception during buy: {str(e)}"
        }


@mcp.tool()
async def sell_live(symbol: str, amount: int) -> Dict[str, Any]:
    """
    Place a live sell order for stocks or cryptocurrency

    This function executes a REAL trade on connected brokerage account.
    It includes position validation before execution.

    ⚠️ WARNING: This will affect real holdings in live trading mode!

    Args:
        symbol: Stock/crypto symbol (e.g., "AAPL", "BTCUSDT")
        amount: Quantity to sell (must be positive integer)

    Returns:
        Dict containing:
        - success: Whether order was placed
        - order_id: Broker's order ID
        - message: Status message
        - order_details: Full order information

    Example:
        >>> result = await sell_live("AAPL", 5)
        >>> print(result)  # {"success": True, "order_id": "...", ...}
    """
    try:
        # Get instances
        broker = await _get_broker()
        provider = await _get_provider()
        risk_manager = await _get_risk_manager()

        # Validate amount
        try:
            amount = int(amount)
            if amount <= 0:
                return {"success": False, "error": "Amount must be positive"}
        except ValueError:
            return {"success": False, "error": "Amount must be an integer"}

        # Check position
        position_qty = await broker.get_position(symbol)
        if position_qty is None or position_qty < amount:
            return {
                "success": False,
                "error": f"Insufficient position: {position_qty or 0} < {amount}"
            }

        # Get current price
        price_data = await provider.get_realtime_price(symbol)
        if not price_data:
            return {"success": False, "error": f"Could not get price for {symbol}"}

        price = price_data.sell_price or price_data.close

        # Place order (no risk check for sells, but could add)
        order = await broker.place_order(
            symbol=symbol,
            side=OrderSide.SELL,
            quantity=amount,
            order_type=OrderType.MARKET
        )

        if not order:
            return {"success": False, "error": "Order placement failed"}

        # Increment trade counter
        risk_manager.increment_trade_count()

        return {
            "success": True,
            "order_id": order.order_id,
            "message": f"Sell order placed: {amount} {symbol} @ ${price:.2f}",
            "order_details": order.to_dict()
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Exception during sell: {str(e)}"
        }


@mcp.tool()
async def get_account_status() -> Dict[str, Any]:
    """
    Get current account status including cash, positions, and portfolio value

    Returns:
        Dict containing account information
    """
    try:
        provider = await _get_provider()
        account_info = await provider.get_account_info()

        if not account_info:
            return {"error": "Could not retrieve account information"}

        return account_info.to_dict()

    except Exception as e:
        return {"error": f"Exception: {str(e)}"}


@mcp.tool()
async def emergency_stop(reason: str = "Manual trigger") -> Dict[str, Any]:
    """
    Activate emergency stop to halt all trading

    ⚠️ This will prevent all future trades until deactivated!

    Args:
        reason: Reason for emergency stop

    Returns:
        Dict with confirmation
    """
    try:
        risk_manager = await _get_risk_manager()
        risk_manager.activate_emergency_stop(reason)

        return {
            "success": True,
            "message": "Emergency stop activated",
            "reason": reason
        }

    except Exception as e:
        return {"error": f"Exception: {str(e)}"}


if __name__ == "__main__":
    # Run MCP server
    mcp.run()
