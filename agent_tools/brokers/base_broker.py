"""
Base classes for broker integrations
Defines abstract interface for order execution
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any


class OrderSide(Enum):
    """Order side enumeration"""
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    """Order type enumeration"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(Enum):
    """Order status enumeration"""
    PENDING = "pending"
    NEW = "new"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class Order:
    """Order information"""
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None  # For limit orders
    stop_price: Optional[float] = None  # For stop orders
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: float = 0.0
    filled_avg_price: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    commission: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "order_id": self.order_id,
            "symbol": self.symbol,
            "side": self.side.value,
            "order_type": self.order_type.value,
            "quantity": self.quantity,
            "price": self.price,
            "stop_price": self.stop_price,
            "status": self.status.value,
            "filled_quantity": self.filled_quantity,
            "filled_avg_price": self.filled_avg_price,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "commission": self.commission,
        }


class BaseBroker(ABC):
    """
    Abstract base class for broker integrations

    Implementations must provide:
    - Order placement (market, limit, stop orders)
    - Order cancellation
    - Order status queries
    - Position queries
    - Account information
    """

    def __init__(self, api_key: str, api_secret: str = None, **kwargs):
        """
        Initialize broker with credentials

        Args:
            api_key: API key for authentication
            api_secret: API secret (if required)
            **kwargs: Additional broker-specific parameters
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self._connected = False

    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish connection to broker

        Returns:
            True if connection successful
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to broker"""
        pass

    @abstractmethod
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
        """
        Place a new order

        Args:
            symbol: Trading symbol
            side: Buy or sell
            quantity: Order quantity
            order_type: Type of order (market, limit, etc.)
            price: Limit price (for limit orders)
            stop_price: Stop price (for stop orders)
            **kwargs: Additional broker-specific parameters

        Returns:
            Order object if successful, None otherwise
        """
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an existing order

        Args:
            order_id: Order ID to cancel

        Returns:
            True if cancellation successful
        """
        pass

    @abstractmethod
    async def get_order(self, order_id: str) -> Optional[Order]:
        """
        Get order details

        Args:
            order_id: Order ID to query

        Returns:
            Order object or None if not found
        """
        pass

    @abstractmethod
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """
        Get all open orders

        Args:
            symbol: Filter by symbol (optional)

        Returns:
            List of open Order objects
        """
        pass

    @abstractmethod
    async def get_order_history(
        self,
        symbol: Optional[str] = None,
        limit: int = 100
    ) -> List[Order]:
        """
        Get order history

        Args:
            symbol: Filter by symbol (optional)
            limit: Maximum number of orders to return

        Returns:
            List of historical Order objects
        """
        pass

    @abstractmethod
    async def get_position(self, symbol: str) -> Optional[float]:
        """
        Get current position for a symbol

        Args:
            symbol: Symbol to query

        Returns:
            Position quantity (positive for long, negative for short)
            None if no position
        """
        pass

    @abstractmethod
    async def get_all_positions(self) -> Dict[str, float]:
        """
        Get all current positions

        Returns:
            Dictionary mapping symbols to quantities
        """
        pass

    @abstractmethod
    async def get_buying_power(self) -> float:
        """
        Get available buying power

        Returns:
            Available cash for trading
        """
        pass

    @abstractmethod
    async def validate_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        price: Optional[float] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Validate order before placing (pre-trade checks)

        Args:
            symbol: Trading symbol
            side: Buy or sell
            quantity: Order quantity
            price: Order price (if applicable)

        Returns:
            Tuple of (is_valid, error_message)
        """
        pass

    @property
    def is_connected(self) -> bool:
        """Check if broker is connected"""
        return self._connected

    # Convenience methods for common operations

    async def buy_market(self, symbol: str, quantity: float) -> Optional[Order]:
        """Place market buy order"""
        return await self.place_order(
            symbol=symbol,
            side=OrderSide.BUY,
            quantity=quantity,
            order_type=OrderType.MARKET
        )

    async def sell_market(self, symbol: str, quantity: float) -> Optional[Order]:
        """Place market sell order"""
        return await self.place_order(
            symbol=symbol,
            side=OrderSide.SELL,
            quantity=quantity,
            order_type=OrderType.MARKET
        )

    async def buy_limit(
        self,
        symbol: str,
        quantity: float,
        price: float
    ) -> Optional[Order]:
        """Place limit buy order"""
        return await self.place_order(
            symbol=symbol,
            side=OrderSide.BUY,
            quantity=quantity,
            order_type=OrderType.LIMIT,
            price=price
        )

    async def sell_limit(
        self,
        symbol: str,
        quantity: float,
        price: float
    ) -> Optional[Order]:
        """Place limit sell order"""
        return await self.place_order(
            symbol=symbol,
            side=OrderSide.SELL,
            quantity=quantity,
            order_type=OrderType.LIMIT,
            price=price
        )
