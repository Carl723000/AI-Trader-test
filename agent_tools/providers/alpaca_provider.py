"""
Alpaca market data provider implementation
Supports US stocks with real-time and historical data
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Callable, Dict, Any
import aiohttp
from .base_provider import MarketDataProvider, PriceData, AccountInfo


class AlpacaDataProvider(MarketDataProvider):
    """
    Alpaca Markets data provider

    Features:
    - Real-time stock quotes (US markets)
    - Historical data access
    - Paper trading and live trading support
    - WebSocket streaming

    API Documentation: https://alpaca.markets/docs/
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://paper-api.alpaca.markets",
        data_url: str = "https://data.alpaca.markets",
        **kwargs
    ):
        """
        Initialize Alpaca provider

        Args:
            api_key: Alpaca API key
            api_secret: Alpaca API secret
            base_url: Base URL for trading API (paper or live)
            data_url: Base URL for market data API
        """
        super().__init__(api_key, api_secret, **kwargs)
        self.base_url = base_url
        self.data_url = data_url
        self._session: Optional[aiohttp.ClientSession] = None
        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._subscriptions: Dict[str, Callable] = {}

    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        return {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret,
        }

    async def connect(self) -> bool:
        """Establish connection to Alpaca"""
        try:
            self._session = aiohttp.ClientSession(headers=self._get_headers())
            # Test connection
            async with self._session.get(f"{self.base_url}/v2/account") as resp:
                if resp.status == 200:
                    self._connected = True
                    return True
                else:
                    print(f"Alpaca connection failed: {resp.status}")
                    return False
        except Exception as e:
            print(f"Error connecting to Alpaca: {e}")
            return False

    async def disconnect(self) -> None:
        """Close connection to Alpaca"""
        if self._ws:
            await self._ws.close()
        if self._session:
            await self._session.close()
        self._connected = False

    async def get_realtime_price(self, symbol: str) -> Optional[PriceData]:
        """
        Get current real-time price from Alpaca

        Uses the latest trade and quote data
        """
        if not self._session:
            return None

        try:
            # Get latest trade
            url = f"{self.data_url}/v2/stocks/{symbol}/trades/latest"
            async with self._session.get(url) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                trade = data.get("trade", {})

            # Get latest quote (for bid/ask)
            url = f"{self.data_url}/v2/stocks/{symbol}/quotes/latest"
            async with self._session.get(url) as resp:
                if resp.status != 200:
                    quote = {}
                else:
                    quote_data = await resp.json()
                    quote = quote_data.get("quote", {})

            # Get latest bar (for OHLCV)
            url = f"{self.data_url}/v2/stocks/{symbol}/bars/latest"
            async with self._session.get(url) as resp:
                if resp.status != 200:
                    bar = {}
                else:
                    bar_data = await resp.json()
                    bar = bar_data.get("bar", {})

            # Construct PriceData
            timestamp = datetime.fromisoformat(
                trade.get("t", datetime.now().isoformat()).replace("Z", "+00:00")
            )

            return PriceData(
                symbol=symbol,
                timestamp=timestamp,
                open=float(bar.get("o", trade.get("p", 0))),
                high=float(bar.get("h", trade.get("p", 0))),
                low=float(bar.get("l", trade.get("p", 0))),
                close=float(trade.get("p", 0)),
                volume=float(bar.get("v", trade.get("s", 0))),
                buy_price=float(quote.get("ap", trade.get("p", 0))),  # Ask price
                sell_price=float(quote.get("bp", trade.get("p", 0))),  # Bid price
            )

        except Exception as e:
            print(f"Error getting Alpaca price for {symbol}: {e}")
            return None

    async def get_historical_price(
        self,
        symbol: str,
        date: datetime,
        interval: str = "1d"
    ) -> Optional[PriceData]:
        """
        Get historical price data for specific date

        Args:
            symbol: Stock symbol
            date: Target date
            interval: Time interval (1Day, 1Hour, 5Min, etc.)
        """
        if not self._session:
            return None

        try:
            # Alpaca timeframe format
            timeframe_map = {
                "1d": "1Day",
                "1h": "1Hour",
                "5m": "5Min",
                "1m": "1Min",
            }
            timeframe = timeframe_map.get(interval, "1Day")

            # Date range (get 1 bar at target date)
            start = date.strftime("%Y-%m-%d")
            end = (date + timedelta(days=1)).strftime("%Y-%m-%d")

            url = f"{self.data_url}/v2/stocks/{symbol}/bars"
            params = {
                "start": start,
                "end": end,
                "timeframe": timeframe,
                "limit": 1,
            }

            async with self._session.get(url, params=params) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                bars = data.get("bars", [])

                if not bars:
                    return None

                bar = bars[0]
                timestamp = datetime.fromisoformat(
                    bar["t"].replace("Z", "+00:00")
                )

                return PriceData(
                    symbol=symbol,
                    timestamp=timestamp,
                    open=float(bar["o"]),
                    high=float(bar["h"]),
                    low=float(bar["l"]),
                    close=float(bar["c"]),
                    volume=float(bar["v"]),
                    buy_price=float(bar["c"]),
                    sell_price=float(bar["c"]),
                )

        except Exception as e:
            print(f"Error getting historical price for {symbol}: {e}")
            return None

    async def get_account_info(self) -> Optional[AccountInfo]:
        """Get Alpaca account information"""
        if not self._session:
            return None

        try:
            # Get account info
            async with self._session.get(f"{self.base_url}/v2/account") as resp:
                if resp.status != 200:
                    return None
                account = await resp.json()

            # Get positions
            async with self._session.get(f"{self.base_url}/v2/positions") as resp:
                if resp.status != 200:
                    positions_data = []
                else:
                    positions_data = await resp.json()

            positions = {
                pos["symbol"]: float(pos["qty"])
                for pos in positions_data
            }

            return AccountInfo(
                account_id=account["account_number"],
                cash=float(account["cash"]),
                portfolio_value=float(account["portfolio_value"]),
                buying_power=float(account["buying_power"]),
                positions=positions,
                currency="USD",
            )

        except Exception as e:
            print(f"Error getting Alpaca account info: {e}")
            return None

    async def subscribe_quotes(
        self,
        symbols: List[str],
        callback: Callable[[PriceData], None]
    ) -> bool:
        """
        Subscribe to real-time quotes via WebSocket

        Note: Requires Alpaca Data API subscription for real-time data
        """
        try:
            if not self._ws or self._ws.closed:
                # Connect to WebSocket
                ws_url = "wss://stream.data.alpaca.markets/v2/iex"
                self._ws = await self._session.ws_connect(ws_url)

                # Authenticate
                auth_msg = {
                    "action": "auth",
                    "key": self.api_key,
                    "secret": self.api_secret,
                }
                await self._ws.send_json(auth_msg)

                # Wait for auth response
                auth_resp = await self._ws.receive_json()
                if auth_resp[0].get("T") != "success":
                    print(f"WebSocket auth failed: {auth_resp}")
                    return False

            # Subscribe to quotes
            subscribe_msg = {
                "action": "subscribe",
                "quotes": symbols,
            }
            await self._ws.send_json(subscribe_msg)

            # Store callbacks
            for symbol in symbols:
                self._subscriptions[symbol] = callback

            # Start listener task
            asyncio.create_task(self._ws_listener())

            return True

        except Exception as e:
            print(f"Error subscribing to Alpaca quotes: {e}")
            return False

    async def _ws_listener(self):
        """Listen to WebSocket messages and invoke callbacks"""
        try:
            async for msg in self._ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = msg.json()
                    for item in data:
                        if item.get("T") == "q":  # Quote message
                            symbol = item["S"]
                            if symbol in self._subscriptions:
                                price_data = PriceData(
                                    symbol=symbol,
                                    timestamp=datetime.fromisoformat(
                                        item["t"].replace("Z", "+00:00")
                                    ),
                                    open=float(item.get("ap", 0)),
                                    high=float(item.get("ap", 0)),
                                    low=float(item.get("bp", 0)),
                                    close=float(item.get("ap", 0)),
                                    volume=0,
                                    buy_price=float(item["ap"]),
                                    sell_price=float(item["bp"]),
                                )
                                self._subscriptions[symbol](price_data)
        except Exception as e:
            print(f"WebSocket listener error: {e}")

    async def unsubscribe_quotes(self, symbols: List[str]) -> bool:
        """Unsubscribe from quotes"""
        try:
            if self._ws and not self._ws.closed:
                unsubscribe_msg = {
                    "action": "unsubscribe",
                    "quotes": symbols,
                }
                await self._ws.send_json(unsubscribe_msg)

            for symbol in symbols:
                self._subscriptions.pop(symbol, None)

            return True
        except Exception as e:
            print(f"Error unsubscribing from Alpaca quotes: {e}")
            return False
