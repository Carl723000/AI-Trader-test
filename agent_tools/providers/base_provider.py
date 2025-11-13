"""
Base classes for market data providers
Defines abstract interface for real-time market data access
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any


@dataclass
class PriceData:
    """Market price data structure"""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    buy_price: Optional[float] = None  # Ask price
    sell_price: Optional[float] = None  # Bid price

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format compatible with existing tools"""
        return {
            "symbol": self.symbol,
            "date": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "open": str(self.open),
            "high": str(self.high),
            "low": str(self.low),
            "close": str(self.close),
            "volume": str(self.volume),
            "buy_price": str(self.buy_price or self.close),
            "sell_price": str(self.sell_price or self.close),
        }


@dataclass
class AccountInfo:
    """Trading account information"""
    account_id: str
    cash: float
    portfolio_value: float
    buying_power: float
    positions: Dict[str, float]  # symbol -> quantity
    currency: str = "USD"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "account_id": self.account_id,
            "cash": self.cash,
            "portfolio_value": self.portfolio_value,
            "buying_power": self.buying_power,
            "positions": self.positions,
            "currency": self.currency,
        }


class MarketDataProvider(ABC):
    """
    Abstract base class for market data providers

    Implementations must provide:
    - Real-time price data
    - Historical price data
    - Account information
    - WebSocket subscriptions for live updates
    """

    def __init__(self, api_key: str, api_secret: str = None, **kwargs):
        """
        Initialize provider with credentials

        Args:
            api_key: API key for authentication
            api_secret: API secret (if required)
            **kwargs: Additional provider-specific parameters
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self._connected = False

    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish connection to data provider

        Returns:
            True if connection successful
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to data provider"""
        pass

    @abstractmethod
    async def get_realtime_price(self, symbol: str) -> Optional[PriceData]:
        """
        Get current real-time price for a symbol

        Args:
            symbol: Stock/crypto symbol

        Returns:
            PriceData object or None if not available
        """
        pass

    @abstractmethod
    async def get_historical_price(
        self,
        symbol: str,
        date: datetime,
        interval: str = "1d"
    ) -> Optional[PriceData]:
        """
        Get historical price data for specific date/time

        Args:
            symbol: Stock/crypto symbol
            date: Target date/time
            interval: Time interval (1d, 1h, 5m, etc.)

        Returns:
            PriceData object or None if not available
        """
        pass

    @abstractmethod
    async def get_account_info(self) -> Optional[AccountInfo]:
        """
        Get current account information

        Returns:
            AccountInfo object or None if unavailable
        """
        pass

    @abstractmethod
    async def subscribe_quotes(
        self,
        symbols: List[str],
        callback: Callable[[PriceData], None]
    ) -> bool:
        """
        Subscribe to real-time quote updates via WebSocket

        Args:
            symbols: List of symbols to subscribe
            callback: Function to call when new data arrives

        Returns:
            True if subscription successful
        """
        pass

    @abstractmethod
    async def unsubscribe_quotes(self, symbols: List[str]) -> bool:
        """
        Unsubscribe from quote updates

        Args:
            symbols: List of symbols to unsubscribe

        Returns:
            True if unsubscription successful
        """
        pass

    @property
    def is_connected(self) -> bool:
        """Check if provider is connected"""
        return self._connected

    async def validate_symbol(self, symbol: str) -> bool:
        """
        Validate if symbol is tradable on this provider

        Args:
            symbol: Symbol to validate

        Returns:
            True if symbol is valid
        """
        # Default implementation - can be overridden
        try:
            price = await self.get_realtime_price(symbol)
            return price is not None
        except Exception:
            return False
