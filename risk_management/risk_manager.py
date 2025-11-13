"""
Risk Manager - Core risk management system
Coordinates risk rules and enforces trading constraints
"""

import json
import asyncio
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any
from .risk_rules import (
    RiskRule,
    RiskViolation,
    RiskLevel,
    MaxSingleTradeRule,
    MaxPositionConcentrationRule,
    MaxDailyTradesRule,
    MaxDailyLossRule,
    InsufficientFundsRule,
    TradingHoursRule,
    MinPositionSizeRule,
)


@dataclass
class RiskCheckResult:
    """Result of risk check"""
    approved: bool
    violations: List[RiskViolation]
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "approved": self.approved,
            "violations": [v.to_dict() for v in self.violations],
            "timestamp": self.timestamp.isoformat(),
        }

    def has_critical_violations(self) -> bool:
        """Check if any critical violations exist"""
        return any(v.level == RiskLevel.CRITICAL for v in self.violations)

    def has_error_violations(self) -> bool:
        """Check if any error violations exist"""
        return any(v.level in [RiskLevel.ERROR, RiskLevel.CRITICAL] for v in self.violations)


class RiskManager:
    """
    Core risk management system

    Responsibilities:
    - Enforce trading risk rules
    - Track daily trading activity
    - Monitor portfolio exposure
    - Emergency stop mechanism
    - Risk violation logging
    """

    def __init__(
        self,
        config: Dict[str, Any],
        log_path: Optional[Path] = None
    ):
        """
        Initialize risk manager

        Args:
            config: Risk configuration dictionary
            log_path: Path for risk violation logs
        """
        self.config = config
        self.log_path = log_path or Path("data/risk_logs")
        self.log_path.mkdir(parents=True, exist_ok=True)

        # Initialize risk rules
        self.rules: List[RiskRule] = []
        self._init_rules()

        # Trading state
        self.emergency_stop = False
        self.daily_trade_count = 0
        self.starting_portfolio_value = 0.0
        self.current_date = date.today()

        # Load state if exists
        self._load_state()

    def _init_rules(self):
        """Initialize risk rules from configuration"""
        risk_config = self.config.get("risk_controls", {})

        # Single trade size limit
        if risk_config.get("enable_max_single_trade", True):
            self.rules.append(
                MaxSingleTradeRule(
                    max_pct=risk_config.get("max_single_trade_pct", 0.10),
                    enabled=True
                )
            )

        # Position concentration limit
        if risk_config.get("enable_max_position", True):
            self.rules.append(
                MaxPositionConcentrationRule(
                    max_pct=risk_config.get("max_position_pct", 0.30),
                    enabled=True
                )
            )

        # Daily trade count limit
        if risk_config.get("enable_max_daily_trades", True):
            self.rules.append(
                MaxDailyTradesRule(
                    max_trades=risk_config.get("max_daily_trades", 50),
                    enabled=True
                )
            )

        # Daily loss limit
        if risk_config.get("enable_max_daily_loss", True):
            self.rules.append(
                MaxDailyLossRule(
                    max_loss_pct=risk_config.get("max_daily_loss_pct", 0.05),
                    enabled=True
                )
            )

        # Insufficient funds check
        self.rules.append(InsufficientFundsRule(enabled=True))

        # Trading hours check
        if risk_config.get("enable_trading_hours", False):
            hours = risk_config.get("trading_hours", (9, 16))
            self.rules.append(
                TradingHoursRule(
                    allowed_hours=hours,
                    enabled=True
                )
            )

        # Minimum position size
        if risk_config.get("enable_min_position_size", True):
            self.rules.append(
                MinPositionSizeRule(
                    min_value=risk_config.get("min_position_value", 10.0),
                    enabled=True
                )
            )

    async def check_trade(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        account_info: Dict[str, Any]
    ) -> RiskCheckResult:
        """
        Check if trade passes all risk rules

        Args:
            symbol: Trading symbol
            side: "buy" or "sell"
            quantity: Trade quantity
            price: Trade price
            account_info: Account information (cash, positions, portfolio_value)

        Returns:
            RiskCheckResult with approval status and violations
        """
        # Check emergency stop
        if self.emergency_stop:
            violation = RiskViolation(
                rule_name="EmergencyStop",
                level=RiskLevel.CRITICAL,
                message="Emergency stop is active - all trading is halted",
                timestamp=datetime.now()
            )
            return RiskCheckResult(
                approved=False,
                violations=[violation],
                timestamp=datetime.now()
            )

        # Reset daily counters if new day
        self._check_new_day(account_info.get("portfolio_value", 0))

        # Build trade parameters
        trade_params = {
            "symbol": symbol,
            "side": side.lower(),
            "quantity": quantity,
            "price": price,
        }

        # Build context
        context = {
            "cash": account_info.get("cash", 0),
            "positions": account_info.get("positions", {}),
            "portfolio_value": account_info.get("portfolio_value", 0),
            "starting_portfolio_value": self.starting_portfolio_value,
            "daily_trade_count": self.daily_trade_count,
        }

        # Run all risk checks
        violations = []
        for rule in self.rules:
            violation = rule.check(trade_params, context)
            if violation:
                violations.append(violation)

        # Determine approval
        # Block if any ERROR or CRITICAL violations
        has_blocking_violations = any(
            v.level in [RiskLevel.ERROR, RiskLevel.CRITICAL]
            for v in violations
        )

        approved = not has_blocking_violations

        result = RiskCheckResult(
            approved=approved,
            violations=violations,
            timestamp=datetime.now()
        )

        # Log result
        await self._log_risk_check(trade_params, result)

        return result

    def increment_trade_count(self):
        """Increment daily trade counter"""
        self.daily_trade_count += 1
        self._save_state()

    def activate_emergency_stop(self, reason: str = "Manual activation"):
        """Activate emergency stop to halt all trading"""
        self.emergency_stop = True
        self._save_state()

        violation = RiskViolation(
            rule_name="EmergencyStop",
            level=RiskLevel.CRITICAL,
            message=f"Emergency stop activated: {reason}",
            timestamp=datetime.now()
        )

        asyncio.create_task(self._log_violation(violation))
        print(f"🚨 EMERGENCY STOP ACTIVATED: {reason}")

    def deactivate_emergency_stop(self):
        """Deactivate emergency stop"""
        self.emergency_stop = False
        self._save_state()
        print("✅ Emergency stop deactivated")

    def _check_new_day(self, current_portfolio_value: float):
        """Check if it's a new trading day and reset counters"""
        today = date.today()

        if today > self.current_date:
            print(f"📅 New trading day: {today}")
            self.current_date = today
            self.daily_trade_count = 0
            self.starting_portfolio_value = current_portfolio_value
            self._save_state()

    def _save_state(self):
        """Save risk manager state"""
        state_file = self.log_path / "risk_state.json"
        state = {
            "emergency_stop": self.emergency_stop,
            "daily_trade_count": self.daily_trade_count,
            "starting_portfolio_value": self.starting_portfolio_value,
            "current_date": self.current_date.isoformat(),
        }

        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)

    def _load_state(self):
        """Load risk manager state"""
        state_file = self.log_path / "risk_state.json"

        if state_file.exists():
            try:
                with open(state_file, "r") as f:
                    state = json.load(f)

                self.emergency_stop = state.get("emergency_stop", False)
                self.daily_trade_count = state.get("daily_trade_count", 0)
                self.starting_portfolio_value = state.get("starting_portfolio_value", 0.0)

                saved_date = state.get("current_date")
                if saved_date:
                    self.current_date = date.fromisoformat(saved_date)

                # Reset if different day
                if self.current_date < date.today():
                    self.daily_trade_count = 0
                    self.current_date = date.today()

            except Exception as e:
                print(f"Warning: Could not load risk state: {e}")

    async def _log_risk_check(self, trade_params: Dict[str, Any], result: RiskCheckResult):
        """Log risk check result"""
        log_file = self.log_path / f"risk_checks_{date.today()}.jsonl"

        log_entry = {
            "timestamp": result.timestamp.isoformat(),
            "trade_params": trade_params,
            "approved": result.approved,
            "violations": [v.to_dict() for v in result.violations],
        }

        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    async def _log_violation(self, violation: RiskViolation):
        """Log risk violation"""
        log_file = self.log_path / f"violations_{date.today()}.jsonl"

        with open(log_file, "a") as f:
            f.write(json.dumps(violation.to_dict()) + "\n")

    def get_stats(self) -> Dict[str, Any]:
        """Get risk manager statistics"""
        return {
            "emergency_stop": self.emergency_stop,
            "daily_trade_count": self.daily_trade_count,
            "starting_portfolio_value": self.starting_portfolio_value,
            "current_date": self.current_date.isoformat(),
            "active_rules": [rule.name for rule in self.rules if rule.enabled],
        }
