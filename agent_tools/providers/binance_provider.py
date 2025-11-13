"""
Binance market data provider implementation
Supports cryptocurrency trading with real-time data
"""

import asyncio
import hmac
import hashlib
import time
from datetime import datetime, timedelta
from typing import List, Optional, Callable, Dict, Any
import aiohttp
from .base_provider import MarketDataProvider, PriceData, AccountInfo


class BinanceDataProvider(MarketDataProvider):
    """
    Binance Exchange data provider

    Features:
    - Real-time crypto quotes
    - Historical kline/candlestick data
    - Spot and futures trading support
    - WebSocket streaming

    API Documentation: https://binance-docs.github.io/apidocs/
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.binance.com",
        ws_url: str = "wss://stream.binance.com:9443",
        testnet: bool = False,
        **kwargs
    ):
        """
        Initialize Binance provider

        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            base_url: Base URL for REST API
            ws_url: Base URL for WebSocket
            testnet: Use testnet (for testing)
        """
        super().__init__(api_key, api_secret, **kwargs)

        if testnet:
            self.base_url = "https://testnet.binance.vision"
            self.ws_url = "wss://testnet.binance.vision"
        else:
            self.base_url = base_url
            self.ws_url = ws_url

        self._session: Optional[aiohttp.ClientSession] = None
        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._subscriptions: Dict[str, Callable] = {}

    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        return {
            "X-MBX-APIKEY": self.api_key,
        }

    def _sign_request(self, params: Dict[str, Any]) -> str:
        """Sign request with HMAC SHA256"""
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

    async def connect(self) -> bool:
        """Establish connection to Binance"""
        try:
            self._session = aiohttp.ClientSession(headers=self._get_headers())
            # Test connection
            async with self._session.get(f"{self.base_url}/api/v3/ping") as resp:
                if resp.status == 200:
                    self._connected = True
                    return True
                else:
                    print(f"Binance connection failed: {resp.status}")
                    return False
        except Exception as e:
            print(f"Error connecting to Binance: {e}")
            return False

    async def disconnect(self) -> None:
        """Close connection to Binance"""
        if self._ws:
            await self._ws.close()
        if self._session:
            await self._session.close()
        self._connected = False

    async def get_realtime_price(self, symbol: str) -> Optional[PriceData]:
        """
        Get current real-time price from Binance

        Args:
            symbol: Trading pair (e.g., 'BTCUSDT', 'ETHUSDT')
        """
        if not self._session:
            return None

        try:
            # Normalize symbol (remove hyphen if present)
            symbol = symbol.replace("-", "")

            # Get 24hr ticker (includes OHLCV)
            url = f"{self.base_url}/api/v3/ticker/24hr"
            params = {"symbol": symbol}

            async with self._session.get(url, params=params) as resp:
                if resp.status != 200:
                    print(f"Binance price error for {symbol}: {resp.status}")
                    return None
                data = await resp.json()

            timestamp = datetime.fromtimestamp(data["closeTime"] / 1000)

            return PriceData(
                symbol=symbol,
                timestamp=timestamp,
                open=float(data["openPrice"]),
                high=float(data["highPrice"]),
                low=float(data["lowPrice"]),
                close=float(data["lastPrice"]),
                volume=float(data["volume"]),
                buy_price=float(data["askPrice"]),  # Best ask
                sell_price=float(data["bidPrice"]),  # Best bid
            )

        except Exception as e:
            print(f"Error getting Binance price for {symbol}: {e}")
            return None

    async def get_historical_price(
        self,
        symbol: str,
        date: datetime,
        interval: str = "1d"
    ) -> Optional[PriceData]:
        """
        Get historical kline data for specific date

        Args:
            symbol: Trading pair
            date: Target date
            interval: Kline interval (1m, 5m, 1h, 1d, etc.)
        """
        if not self._session:
            return None

        try:
            # Normalize symbol
            symbol = symbol.replace("-", "")

            # Binance interval format
            interval_map = {
                "1m": "1m",
                "5m": "5m",
                "1h": "1h",
                "1d": "1d",
            }
            binance_interval = interval_map.get(interval, "1d")

            # Convert date to timestamp
            start_time = int(date.timestamp() * 1000)
            end_time = int((date + timedelta(days=1)).timestamp() * 1000)

            url = f"{self.base_url}/api/v3/klines"
            params = {
                "symbol": symbol,
                "interval": binance_interval,
                "startTime": start_time,
                "endTime": end_time,
                "limit": 1,
            }

            async with self._session.get(url, params=params) as resp:
                if resp.status != 200:
                    return None
                klines = await resp.json()

                if not klines:
                    return None

                kline = klines[0]
                # Kline format: [open_time, open, high, low, close, volume, ...]
                timestamp = datetime.fromtimestamp(kline[0] / 1000)

                return PriceData(
                    symbol=symbol,
                    timestamp=timestamp,
                    open=float(kline[1]),
                    high=float(kline[2]),
                    low=float(kline[3]),
                    close=float(kline[4]),
                    volume=float(kline[5]),
                    buy_price=float(kline[4]),
                    sell_price=float(kline[4]),
                )

        except Exception as e:
            print(f"Error getting historical price for {symbol}: {e}")
            return None

    async def get_account_info(self) -> Optional[AccountInfo]:
        """Get Binance account information"""
        if not self._session:
            return None

        try:
            # Sign request
            params = {
                "timestamp": int(time.time() * 1000),
            }
            params["signature"] = self._sign_request(params)

            url = f"{self.base_url}/api/v3/account"
            async with self._session.get(url, params=params) as resp:
                if resp.status != 200:
                    print(f"Binance account error: {resp.status}")
                    return None
                account = await resp.json()

            # Extract USDT balance and positions
            positions = {}
            usdt_balance = 0.0

            for balance in account["balances"]:
                asset = balance["asset"]
                free = float(balance["free"])
                locked = float(balance["locked"])
                total = free + locked

                if asset == "USDT":
                    usdt_balance = total
                elif total > 0:
                    positions[f"{asset}USDT"] = total

            # Calculate portfolio value (simplified)
            portfolio_value = usdt_balance
            for symbol, qty in positions.items():
                price_data = await self.get_realtime_price(symbol)
                if price_data:
                    portfolio_value += qty * price_data.close

            return AccountInfo(
                account_id=account.get("accountType", "SPOT"),
                cash=usdt_balance,
                portfolio_value=portfolio_value,
                buying_power=usdt_balance,
                positions=positions,
                currency="USDT",
            )

        except Exception as e:
            print(f"Error getting Binance account info: {e}")
            return None

    async def subscribe_quotes(
        self,
        symbols: List[str],
        callback: Callable[[PriceData], None]
    ) -> bool:
        """
        Subscribe to real-time ticker updates via WebSocket

        Args:
            symbols: List of trading pairs
            callback: Callback function for price updates
        """
        try:
            # Normalize symbols and create stream names
            streams = []
            for symbol in symbols:
                normalized = symbol.replace("-", "").lower()
                streams.append(f"{normalized}@ticker")

            # Build WebSocket URL
            stream_path = "/".join(streams)
            ws_url = f"{self.ws_url}/stream?streams={stream_path}"

            # Connect to WebSocket
            self._ws = await self._session.ws_connect(ws_url)

            # Store callbacks
            for symbol in symbols:
                normalized = symbol.replace("-", "")
                self._subscriptions[normalized.upper()] = callback

            # Start listener
            asyncio.create_task(self._ws_listener())

            return True

        except Exception as e:
            print(f"Error subscribing to Binance quotes: {e}")
            return False

    async def _ws_listener(self):
        """Listen to WebSocket messages"""
        try:
            async for msg in self._ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = msg.json()
                    if "data" in data:
                        ticker = data["data"]
                        symbol = ticker["s"]  # Symbol

                        if symbol in self._subscriptions:
                            price_data = PriceData(
                                symbol=symbol,
                                timestamp=datetime.fromtimestamp(ticker["E"] / 1000),
                                open=float(ticker["o"]),
                                high=float(ticker["h"]),
                                low=float(ticker["l"]),
                                close=float(ticker["c"]),
                                volume=float(ticker["v"]),
                                buy_price=float(ticker["a"]),  # Best ask
                                sell_price=float(ticker["b"]),  # Best bid
                            )
                            self._subscriptions[symbol](price_data)
        except Exception as e:
            print(f"WebSocket listener error: {e}")

    async def unsubscribe_quotes(self, symbols: List[str]) -> bool:
        """Unsubscribe from quotes"""
        try:
            # Binance WebSocket doesn't support dynamic unsubscribe
            # Need to close and reconnect without these symbols
            for symbol in symbols:
                normalized = symbol.replace("-", "").upper()
                self._subscriptions.pop(normalized, None)

            # If no more subscriptions, close WebSocket
            if not self._subscriptions and self._ws:
                await self._ws.close()
                self._ws = None

            return True
        except Exception as e:
            print(f"Error unsubscribing from Binance quotes: {e}")
            return False
