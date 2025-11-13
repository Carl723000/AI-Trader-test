"""
Alpaca broker implementation for US stocks trading
"""

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


class AlpacaBroker(BaseBroker):
    """
    Alpaca Markets broker implementation

    Features:
    - Market and limit orders
    - Paper trading and live trading
    - Commission-free US stocks
    - Real-time order status

    API Documentation: https://alpaca.markets/docs/
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://paper-api.alpaca.markets",
        **kwargs
    ):
        """
        Initialize Alpaca broker

        Args:
            api_key: Alpaca API key
            api_secret: Alpaca API secret
            base_url: Base URL (paper or live trading)
        """
        super().__init__(api_key, api_secret, **kwargs)
        self.base_url = base_url
        self._session: Optional[aiohttp.ClientSession] = None

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
        """Close connection"""
        if self._session:
            await self._session.close()
        self._connected = False

    def _parse_order(self, data: Dict[str, Any]) -> Order:
        """Parse Alpaca order response to Order object"""
        # Map Alpaca status to our OrderStatus
        status_map = {
            "new": OrderStatus.NEW,
            "partially_filled": OrderStatus.PARTIALLY_FILLED,
            "filled": OrderStatus.FILLED,
            "canceled": OrderStatus.CANCELED,
            "rejected": OrderStatus.REJECTED,
            "expired": OrderStatus.EXPIRED,
            "pending_new": OrderStatus.PENDING,
        }

        # Map Alpaca order type
        type_map = {
            "market": OrderType.MARKET,
            "limit": OrderType.LIMIT,
            "stop": OrderType.STOP,
            "stop_limit": OrderType.STOP_LIMIT,
        }

        return Order(
            order_id=data["id"],
            symbol=data["symbol"],
            side=OrderSide.BUY if data["side"] == "buy" else OrderSide.SELL,
            order_type=type_map.get(data["type"], OrderType.MARKET),
            quantity=float(data["qty"]),
            price=float(data["limit_price"]) if data.get("limit_price") else None,
            stop_price=float(data["stop_price"]) if data.get("stop_price") else None,
            status=status_map.get(data["status"], OrderStatus.PENDING),
            filled_quantity=float(data.get("filled_qty", 0)),
            filled_avg_price=float(data["filled_avg_price"]) if data.get("filled_avg_price") else None,
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00")) if data.get("updated_at") else None,
            commission=0.0,  # Alpaca is commission-free
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
        """Place order with Alpaca"""
        if not self._session:
            print("Not connected to Alpaca")
            return None

        try:
            # Build order payload
            payload = {
                "symbol": symbol,
                "qty": quantity,
                "side": side.value,
                "type": order_type.value,
                "time_in_force": kwargs.get("time_in_force", "day"),
            }

            if order_type == OrderType.LIMIT and price:
                payload["limit_price"] = price
            elif order_type == OrderType.STOP and stop_price:
                payload["stop_price"] = stop_price
            elif order_type == OrderType.STOP_LIMIT and price and stop_price:
                payload["limit_price"] = price
                payload["stop_price"] = stop_price

            # Place order
            url = f"{self.base_url}/v2/orders"
            async with self._session.post(url, json=payload) as resp:
                if resp.status in [200, 201]:
                    data = await resp.json()
                    return self._parse_order(data)
                else:
                    error = await resp.text()
                    print(f"Alpaca order failed: {resp.status} - {error}")
                    return None

        except Exception as e:
            print(f"Error placing Alpaca order: {e}")
            return None

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel order"""
        if not self._session:
            return False

        try:
            url = f"{self.base_url}/v2/orders/{order_id}"
            async with self._session.delete(url) as resp:
                return resp.status in [200, 204]
        except Exception as e:
            print(f"Error canceling Alpaca order: {e}")
            return False

    async def get_order(self, order_id: str) -> Optional[Order]:
        """Get order details"""
        if not self._session:
            return None

        try:
            url = f"{self.base_url}/v2/orders/{order_id}"
            async with self._session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return self._parse_order(data)
                return None
        except Exception as e:
            print(f"Error getting Alpaca order: {e}")
            return None

    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """Get open orders"""
        if not self._session:
            return []

        try:
            url = f"{self.base_url}/v2/orders"
            params = {"status": "open"}
            if symbol:
                params["symbols"] = symbol

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
            url = f"{self.base_url}/v2/orders"
            params = {
                "status": "all",
                "limit": limit,
            }
            if symbol:
                params["symbols"] = symbol

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
        if not self._session:
            return None

        try:
            url = f"{self.base_url}/v2/positions/{symbol}"
            async with self._session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return float(data["qty"])
                elif resp.status == 404:
                    return 0.0  # No position
                return None
        except Exception as e:
            print(f"Error getting position: {e}")
            return None

    async def get_all_positions(self) -> Dict[str, float]:
        """Get all positions"""
        if not self._session:
            return {}

        try:
            url = f"{self.base_url}/v2/positions"
            async with self._session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {pos["symbol"]: float(pos["qty"]) for pos in data}
                return {}
        except Exception as e:
            print(f"Error getting positions: {e}")
            return {}

    async def get_buying_power(self) -> float:
        """Get available buying power"""
        if not self._session:
            return 0.0

        try:
            url = f"{self.base_url}/v2/account"
            async with self._session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return float(data["buying_power"])
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

        # Check buying power for buy orders
        if side == OrderSide.BUY:
            buying_power = await self.get_buying_power()
            estimated_cost = quantity * (price if price else 0)

            if price and estimated_cost > buying_power:
                return False, f"Insufficient buying power: ${buying_power:.2f} < ${estimated_cost:.2f}"

        # Check position for sell orders
        if side == OrderSide.SELL:
            position = await self.get_position(symbol)
            if position is None:
                return False, "Unable to retrieve position"
            if position < quantity:
                return False, f"Insufficient position: {position} < {quantity}"

        # Quantity validation
        if quantity <= 0:
            return False, "Quantity must be positive"

        return True, None
