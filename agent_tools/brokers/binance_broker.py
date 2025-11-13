"""
Binance broker implementation for cryptocurrency trading
"""

import hmac
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import aiohttp
from .base_broker import (
    BaseBroker,
    Order,
    OrderSide,
    OrderType,
    OrderStatus
)


class BinanceBroker(BaseBroker):
    """
    Binance Exchange broker implementation

    Features:
    - Spot trading for cryptocurrencies
    - Market and limit orders
    - Real-time order status
    - Testnet support for testing

    API Documentation: https://binance-docs.github.io/apidocs/
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.binance.com",
        testnet: bool = False,
        **kwargs
    ):
        """
        Initialize Binance broker

        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            base_url: Base URL for API
            testnet: Use testnet for testing
        """
        super().__init__(api_key, api_secret, **kwargs)

        if testnet:
            self.base_url = "https://testnet.binance.vision"
        else:
            self.base_url = base_url

        self._session: Optional[aiohttp.ClientSession] = None

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
        """Close connection"""
        if self._session:
            await self._session.close()
        self._connected = False

    def _parse_order(self, data: Dict[str, Any]) -> Order:
        """Parse Binance order response to Order object"""
        # Map Binance status
        status_map = {
            "NEW": OrderStatus.NEW,
            "PARTIALLY_FILLED": OrderStatus.PARTIALLY_FILLED,
            "FILLED": OrderStatus.FILLED,
            "CANCELED": OrderStatus.CANCELED,
            "REJECTED": OrderStatus.REJECTED,
            "EXPIRED": OrderStatus.EXPIRED,
            "PENDING_CANCEL": OrderStatus.PENDING,
        }

        # Map order type
        type_map = {
            "MARKET": OrderType.MARKET,
            "LIMIT": OrderType.LIMIT,
            "STOP_LOSS": OrderType.STOP,
            "STOP_LOSS_LIMIT": OrderType.STOP_LIMIT,
        }

        return Order(
            order_id=str(data["orderId"]),
            symbol=data["symbol"],
            side=OrderSide.BUY if data["side"] == "BUY" else OrderSide.SELL,
            order_type=type_map.get(data["type"], OrderType.MARKET),
            quantity=float(data["origQty"]),
            price=float(data["price"]) if data.get("price") and float(data["price"]) > 0 else None,
            stop_price=float(data["stopPrice"]) if data.get("stopPrice") and float(data["stopPrice"]) > 0 else None,
            status=status_map.get(data["status"], OrderStatus.PENDING),
            filled_quantity=float(data.get("executedQty", 0)),
            filled_avg_price=float(data.get("avgPrice", 0)) if data.get("avgPrice") else None,
            created_at=datetime.fromtimestamp(data["time"] / 1000) if "time" in data else None,
            updated_at=datetime.fromtimestamp(data["updateTime"] / 1000) if "updateTime" in data else None,
            commission=0.0,  # Commission calculated separately
        )

    async def place_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        order_type: OrderType = OrderType.MARKET,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        **kwargs
    ) -> Optional[Order]:
        """Place order with Binance"""
        if not self._session:
            print("Not connected to Binance")
            return None

        try:
            # Normalize symbol (remove hyphen)
            symbol = symbol.replace("-", "")

            # Build order parameters
            params = {
                "symbol": symbol,
                "side": "BUY" if side == OrderSide.BUY else "SELL",
                "type": order_type.value.upper(),
                "timestamp": int(time.time() * 1000),
            }

            # Quantity (Binance uses different param names)
            if order_type == OrderType.MARKET and side == OrderSide.BUY:
                # For market buy, can use quoteOrderQty (amount in USDT)
                # Or quantity (amount in base asset)
                params["quantity"] = quantity
            else:
                params["quantity"] = quantity

            # Time in force (required for limit orders)
            if order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]:
                params["timeInForce"] = kwargs.get("timeInForce", "GTC")

            # Prices
            if order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT] and price:
                params["price"] = price

            if order_type in [OrderType.STOP, OrderType.STOP_LIMIT] and stop_price:
                params["stopPrice"] = stop_price

            # Sign request
            params["signature"] = self._sign_request(params)

            # Place order
            url = f"{self.base_url}/api/v3/order"
            async with self._session.post(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return self._parse_order(data)
                else:
                    error = await resp.text()
                    print(f"Binance order failed: {resp.status} - {error}")
                    return None

        except Exception as e:
            print(f"Error placing Binance order: {e}")
            return None

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel order"""
        if not self._session:
            return False

        try:
            params = {
                "orderId": order_id,
                "timestamp": int(time.time() * 1000),
            }
            params["signature"] = self._sign_request(params)

            url = f"{self.base_url}/api/v3/order"
            async with self._session.delete(url, params=params) as resp:
                return resp.status == 200
        except Exception as e:
            print(f"Error canceling Binance order: {e}")
            return False

    async def get_order(self, order_id: str) -> Optional[Order]:
        """Get order details"""
        if not self._session:
            return None

        try:
            params = {
                "orderId": order_id,
                "timestamp": int(time.time() * 1000),
            }
            params["signature"] = self._sign_request(params)

            url = f"{self.base_url}/api/v3/order"
            async with self._session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return self._parse_order(data)
                return None
        except Exception as e:
            print(f"Error getting Binance order: {e}")
            return None

    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """Get open orders"""
        if not self._session:
            return []

        try:
            params = {
                "timestamp": int(time.time() * 1000),
            }
            if symbol:
                params["symbol"] = symbol.replace("-", "")

            params["signature"] = self._sign_request(params)

            url = f"{self.base_url}/api/v3/openOrders"
            async with self._session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return [self._parse_order(order) for order in data]
                return []
        except Exception as e:
            print(f"Error getting open orders: {e}")
            return []

    async def get_order_history(
        self,
        symbol: Optional[str] = None,
        limit: int = 100
    ) -> List[Order]:
        """Get order history"""
        if not self._session:
            return []

        try:
            if not symbol:
                return []  # Binance requires symbol for order history

            params = {
                "symbol": symbol.replace("-", ""),
                "limit": limit,
                "timestamp": int(time.time() * 1000),
            }
            params["signature"] = self._sign_request(params)

            url = f"{self.base_url}/api/v3/allOrders"
            async with self._session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return [self._parse_order(order) for order in data]
                return []
        except Exception as e:
            print(f"Error getting order history: {e}")
            return []

    async def get_position(self, symbol: str) -> Optional[float]:
        """Get position quantity"""
        positions = await self.get_all_positions()
        normalized = symbol.replace("-", "")
        return positions.get(normalized, 0.0)

    async def get_all_positions(self) -> Dict[str, float]:
        """Get all positions"""
        if not self._session:
            return {}

        try:
            params = {
                "timestamp": int(time.time() * 1000),
            }
            params["signature"] = self._sign_request(params)

            url = f"{self.base_url}/api/v3/account"
            async with self._session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    positions = {}
                    for balance in data["balances"]:
                        asset = balance["asset"]
                        free = float(balance["free"])
                        locked = float(balance["locked"])
                        total = free + locked

                        if total > 0 and asset != "USDT":
                            # Format as trading pair
                            positions[f"{asset}USDT"] = total

                    return positions
                return {}
        except Exception as e:
            print(f"Error getting positions: {e}")
            return {}

    async def get_buying_power(self) -> float:
        """Get available USDT balance"""
        if not self._session:
            return 0.0

        try:
            params = {
                "timestamp": int(time.time() * 1000),
            }
            params["signature"] = self._sign_request(params)

            url = f"{self.base_url}/api/v3/account"
            async with self._session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for balance in data["balances"]:
                        if balance["asset"] == "USDT":
                            return float(balance["free"])
                return 0.0
        except Exception as e:
            print(f"Error getting buying power: {e}")
            return 0.0

    async def validate_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        price: Optional[float] = None
    ) -> tuple[bool, Optional[str]]:
        """Validate order"""
        if not self._session:
            return False, "Not connected to broker"

        # Normalize symbol
        symbol = symbol.replace("-", "")

        # Check buying power for buy orders
        if side == OrderSide.BUY:
            buying_power = await self.get_buying_power()
            estimated_cost = quantity * (price if price else 0)

            if price and estimated_cost > buying_power:
                return False, f"Insufficient USDT: {buying_power:.2f} < {estimated_cost:.2f}"

        # Check position for sell orders
        if side == OrderSide.SELL:
            position = await self.get_position(symbol)
            if position is None:
                return False, "Unable to retrieve position"
            if position < quantity:
                return False, f"Insufficient {symbol}: {position} < {quantity}"

        # Quantity validation
        if quantity <= 0:
            return False, "Quantity must be positive"

        return True, None
