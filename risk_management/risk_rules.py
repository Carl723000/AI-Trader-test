"""
Risk rules and violations for trading risk management
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional


class RiskLevel(Enum):
    """Risk violation severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class RiskViolation:
    """Risk rule violation"""
    rule_name: str
    level: RiskLevel
    message: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "rule_name": self.rule_name,
            "level": self.level.value,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details or {},
        }


class RiskRule(ABC):
    """
    Abstract base class for risk rules

    Each rule implements a specific risk check
    """

    def __init__(self, name: str, enabled: bool = True):
        """
        Initialize risk rule

        Args:
            name: Rule name
            enabled: Whether rule is enabled
        """
        self.name = name
        self.enabled = enabled

    @abstractmethod
    def check(self, trade_params: Dict[str, Any], context: Dict[str, Any]) -> Optional[RiskViolation]:
        """
        Check if trade violates this risk rule

        Args:
            trade_params: Trade parameters (symbol, side, quantity, price, etc.)
            context: Additional context (account info, positions, market data, etc.)

        Returns:
            RiskViolation if rule is violated, None otherwise
        """
        pass


class MaxSingleTradeRule(RiskRule):
    """Maximum single trade size as percentage of portfolio"""

    def __init__(self, max_pct: float = 0.10, enabled: bool = True):
        """
        Args:
            max_pct: Maximum percentage of portfolio for single trade (default 10%)
        """
        super().__init__("MaxSingleTrade", enabled)
        self.max_pct = max_pct

    def check(self, trade_params: Dict[str, Any], context: Dict[str, Any]) -> Optional[RiskViolation]:
        if not self.enabled:
            return None

        quantity = trade_params.get("quantity", 0)
        price = trade_params.get("price", 0)
        side = trade_params.get("side", "")

        if side != "buy":
            return None  # Only check for buy orders

        portfolio_value = context.get("portfolio_value", 0)
        if portfolio_value == 0:
            return None

        trade_value = quantity * price
        trade_pct = trade_value / portfolio_value

        if trade_pct > self.max_pct:
            return RiskViolation(
                rule_name=self.name,
                level=RiskLevel.ERROR,
                message=f"Trade size {trade_pct*100:.1f}% exceeds maximum {self.max_pct*100:.1f}%",
                timestamp=datetime.now(),
                details={
                    "trade_value": trade_value,
                    "portfolio_value": portfolio_value,
                    "trade_pct": trade_pct,
                    "max_pct": self.max_pct,
                }
            )

        return None


class MaxPositionConcentrationRule(RiskRule):
    """Maximum position concentration for single symbol"""

    def __init__(self, max_pct: float = 0.30, enabled: bool = True):
        """
        Args:
            max_pct: Maximum percentage of portfolio in single position (default 30%)
        """
        super().__init__("MaxPositionConcentration", enabled)
        self.max_pct = max_pct

    def check(self, trade_params: Dict[str, Any], context: Dict[str, Any]) -> Optional[RiskViolation]:
        if not self.enabled:
            return None

        symbol = trade_params.get("symbol", "")
        quantity = trade_params.get("quantity", 0)
        price = trade_params.get("price", 0)
        side = trade_params.get("side", "")

        if side != "buy":
            return None

        portfolio_value = context.get("portfolio_value", 0)
        positions = context.get("positions", {})

        # Calculate position value after trade
        current_qty = positions.get(symbol, 0)
        new_qty = current_qty + quantity
        new_position_value = new_qty * price

        if portfolio_value == 0:
            return None

        position_pct = new_position_value / portfolio_value

        if position_pct > self.max_pct:
            return RiskViolation(
                rule_name=self.name,
                level=RiskLevel.ERROR,
                message=f"Position {symbol} would be {position_pct*100:.1f}% (max {self.max_pct*100:.1f}%)",
                timestamp=datetime.now(),
                details={
                    "symbol": symbol,
                    "position_value": new_position_value,
                    "portfolio_value": portfolio_value,
                    "position_pct": position_pct,
                    "max_pct": self.max_pct,
                }
            )

        return None


class MaxDailyTradesRule(RiskRule):
    """Maximum number of trades per day"""

    def __init__(self, max_trades: int = 50, enabled: bool = True):
        """
        Args:
            max_trades: Maximum trades per day (default 50)
        """
        super().__init__("MaxDailyTrades", enabled)
        self.max_trades = max_trades

    def check(self, trade_params: Dict[str, Any], context: Dict[str, Any]) -> Optional[RiskViolation]:
        if not self.enabled:
            return None

        daily_trades = context.get("daily_trade_count", 0)

        if daily_trades >= self.max_trades:
            return RiskViolation(
                rule_name=self.name,
                level=RiskLevel.ERROR,
                message=f"Daily trade limit reached: {daily_trades}/{self.max_trades}",
                timestamp=datetime.now(),
                details={
                    "daily_trades": daily_trades,
                    "max_trades": self.max_trades,
                }
            )

        return None


class MaxDailyLossRule(RiskRule):
    """Maximum daily loss as percentage of starting capital"""

    def __init__(self, max_loss_pct: float = 0.05, enabled: bool = True):
        """
        Args:
            max_loss_pct: Maximum daily loss percentage (default 5%)
        """
        super().__init__("MaxDailyLoss", enabled)
        self.max_loss_pct = max_loss_pct

    def check(self, trade_params: Dict[str, Any], context: Dict[str, Any]) -> Optional[RiskViolation]:
        if not self.enabled:
            return None

        starting_value = context.get("starting_portfolio_value", 0)
        current_value = context.get("portfolio_value", 0)

        if starting_value == 0:
            return None

        daily_pnl = current_value - starting_value
        daily_pnl_pct = daily_pnl / starting_value

        if daily_pnl_pct <= -self.max_loss_pct:
            return RiskViolation(
                rule_name=self.name,
                level=RiskLevel.CRITICAL,
                message=f"Daily loss {daily_pnl_pct*100:.2f}% exceeds limit {self.max_loss_pct*100:.2f}%",
                timestamp=datetime.now(),
                details={
                    "starting_value": starting_value,
                    "current_value": current_value,
                    "daily_pnl": daily_pnl,
                    "daily_pnl_pct": daily_pnl_pct,
                    "max_loss_pct": self.max_loss_pct,
                }
            )

        return None


class InsufficientFundsRule(RiskRule):
    """Check for sufficient funds"""

    def __init__(self, enabled: bool = True):
        super().__init__("InsufficientFunds", enabled)

    def check(self, trade_params: Dict[str, Any], context: Dict[str, Any]) -> Optional[RiskViolation]:
        if not self.enabled:
            return None

        side = trade_params.get("side", "")
        if side != "buy":
            return None

        quantity = trade_params.get("quantity", 0)
        price = trade_params.get("price", 0)
        cash = context.get("cash", 0)

        trade_cost = quantity * price

        if trade_cost > cash:
            return RiskViolation(
                rule_name=self.name,
                level=RiskLevel.ERROR,
                message=f"Insufficient funds: ${cash:.2f} < ${trade_cost:.2f}",
                timestamp=datetime.now(),
                details={
                    "cash": cash,
                    "trade_cost": trade_cost,
                    "shortfall": trade_cost - cash,
                }
            )

        return None


class TradingHoursRule(RiskRule):
    """Check if trading is allowed during current hours"""

    def __init__(self, allowed_hours: tuple = (9, 16), enabled: bool = True):
        """
        Args:
            allowed_hours: Tuple of (start_hour, end_hour) in 24h format
        """
        super().__init__("TradingHours", enabled)
        self.start_hour, self.end_hour = allowed_hours

    def check(self, trade_params: Dict[str, Any], context: Dict[str, Any]) -> Optional[RiskViolation]:
        if not self.enabled:
            return None

        now = datetime.now()
        current_hour = now.hour

        if not (self.start_hour <= current_hour < self.end_hour):
            return RiskViolation(
                rule_name=self.name,
                level=RiskLevel.WARNING,
                message=f"Trading outside allowed hours ({self.start_hour}:00-{self.end_hour}:00)",
                timestamp=now,
                details={
                    "current_hour": current_hour,
                    "allowed_hours": (self.start_hour, self.end_hour),
                }
            )

        return None


class MinPositionSizeRule(RiskRule):
    """Minimum position size to avoid dust trades"""

    def __init__(self, min_value: float = 10.0, enabled: bool = True):
        """
        Args:
            min_value: Minimum trade value (default $10)
        """
        super().__init__("MinPositionSize", enabled)
        self.min_value = min_value

    def check(self, trade_params: Dict[str, Any], context: Dict[str, Any]) -> Optional[RiskViolation]:
        if not self.enabled:
            return None

        quantity = trade_params.get("quantity", 0)
        price = trade_params.get("price", 0)
        trade_value = quantity * price

        if trade_value < self.min_value:
            return RiskViolation(
                rule_name=self.name,
                level=RiskLevel.WARNING,
                message=f"Trade value ${trade_value:.2f} below minimum ${self.min_value:.2f}",
                timestamp=datetime.now(),
                details={
                    "trade_value": trade_value,
                    "min_value": self.min_value,
                }
            )

        return None
