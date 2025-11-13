"""
Live Price Tool - MCP tool for real-time price data
Gets current market prices from live data providers
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional

from fastmcp import FastMCP
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tools.general_tools import get_config_value
from agent_tools.providers import MarketDataProvider, AlpacaDataProvider, BinanceDataProvider

load_dotenv()

mcp = FastMCP("LivePrices")

# Global provider instance
_provider: Optional[MarketDataProvider] = None


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
                data_url = "https://data.alpaca.markets"
            else:
                base_url = "https://paper-api.alpaca.markets"
                data_url = "https://data.alpaca.markets"

            _provider = AlpacaDataProvider(
                api_key,
                api_secret,
                base_url=base_url,
                data_url=data_url
            )

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

        print(f"✅ Connected to {broker_type} live data provider ({trading_mode} mode)")

    return _provider


@mcp.tool()
async def get_price_live(symbol: str) -> Dict[str, Any]:
    """
    Get current real-time price for stock or cryptocurrency

    This function returns LIVE market data from the connected data provider.

    Args:
        symbol: Stock/crypto symbol (e.g., "AAPL", "BTCUSDT", "600519.SH")

    Returns:
        Dictionary containing:
        - symbol: Trading symbol
        - timestamp: Current timestamp
        - open: Opening price
        - high: High price
        - low: Low price
        - close: Current/last price
        - volume: Trading volume
        - buy_price: Best ask price
        - sell_price: Best bid price

    Example:
        >>> result = await get_price_live("AAPL")
        >>> print(result)
        {
            "symbol": "AAPL",
            "timestamp": "2025-11-13 14:30:00",
            "open": "225.50",
            "high": "227.80",
            "low": "225.10",
            "close": "226.45",
            "volume": "12345678",
            "buy_price": "226.46",
            "sell_price": "226.44"
        }
    """
    try:
        provider = await _get_provider()

        # Get real-time price
        price_data = await provider.get_realtime_price(symbol)

        if not price_data:
            return {
                "error": f"Could not get price data for {symbol}",
                "symbol": symbol
            }

        # Convert to dictionary format compatible with existing tools
        return price_data.to_dict()

    except Exception as e:
        return {
            "error": f"Exception getting price: {str(e)}",
            "symbol": symbol
        }


@mcp.tool()
async def get_price_historical(symbol: str, date: str) -> Dict[str, Any]:
    """
    Get historical price data for specific date

    Args:
        symbol: Stock/crypto symbol
        date: Date in 'YYYY-MM-DD' format

    Returns:
        Dictionary containing OHLCV data for the specified date

    Example:
        >>> result = await get_price_historical("AAPL", "2025-11-12")
        >>> print(result)
        {
            "symbol": "AAPL",
            "date": "2025-11-12",
            "open": "224.50",
            ...
        }
    """
    try:
        provider = await _get_provider()

        # Parse date
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}

        # Get historical price
        price_data = await provider.get_historical_price(symbol, target_date)

        if not price_data:
            return {
                "error": f"No data available for {symbol} on {date}",
                "symbol": symbol,
                "date": date
            }

        return price_data.to_dict()

    except Exception as e:
        return {
            "error": f"Exception getting historical price: {str(e)}",
            "symbol": symbol,
            "date": date
        }


@mcp.tool()
async def get_multiple_prices(symbols: list) -> Dict[str, Any]:
    """
    Get real-time prices for multiple symbols at once

    Args:
        symbols: List of trading symbols

    Returns:
        Dictionary mapping symbols to their price data

    Example:
        >>> result = await get_multiple_prices(["AAPL", "MSFT", "GOOGL"])
        >>> print(result)
        {
            "AAPL": {"close": "226.45", ...},
            "MSFT": {"close": "415.30", ...},
            ...
        }
    """
    try:
        provider = await _get_provider()

        results = {}
        for symbol in symbols:
            price_data = await provider.get_realtime_price(symbol)
            if price_data:
                results[symbol] = price_data.to_dict()
            else:
                results[symbol] = {"error": "No data available"}

        return results

    except Exception as e:
        return {"error": f"Exception: {str(e)}"}


if __name__ == "__main__":
    # Run MCP server
    mcp.run()
