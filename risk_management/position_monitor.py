"""
Position Monitor - Track and manage trading positions in real-time
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class PositionMonitor:
    """
    Monitor trading positions and exposure

    Features:
    - Track all open positions
    - Calculate position metrics
    - Monitor stop-loss levels
    - Alert on position changes
    """

    def __init__(self, log_path: Optional[Path] = None):
        """
        Initialize position monitor

        Args:
            log_path: Path for position logs
        """
        self.log_path = log_path or Path("data/position_logs")
        self.log_path.mkdir(parents=True, exist_ok=True)

        self.positions: Dict[str, Dict[str, Any]] = {}
        self.stop_loss_levels: Dict[str, float] = {}

    def update_position(
        self,
        symbol: str,
        quantity: float,
        avg_price: float,
        current_price: Optional[float] = None
    ):
        """
        Update position information

        Args:
            symbol: Trading symbol
            quantity: Current quantity
            avg_price: Average entry price
            current_price: Current market price (optional)
        """
        self.positions[symbol] = {
            "quantity": quantity,
            "avg_price": avg_price,
            "current_price": current_price or avg_price,
            "updated_at": datetime.now().isoformat(),
        }

        self._log_position_update(symbol)

    def remove_position(self, symbol: str):
        """Remove closed position"""
        if symbol in self.positions:
            del self.positions[symbol]
            self.stop_loss_levels.pop(symbol, None)
            self._log_position_update(symbol, closed=True)

    def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get position details"""
        return self.positions.get(symbol)

    def get_all_positions(self) -> Dict[str, Dict[str, Any]]:
        """Get all positions"""
        return self.positions.copy()

    def calculate_pnl(self, symbol: str, current_price: float) -> Optional[float]:
        """
        Calculate unrealized P&L for position

        Args:
            symbol: Trading symbol
            current_price: Current market price

        Returns:
            P&L amount or None if no position
        """
        position = self.positions.get(symbol)
        if not position:
            return None

        quantity = position["quantity"]
        avg_price = position["avg_price"]

        pnl = (current_price - avg_price) * quantity
        return pnl

    def calculate_pnl_pct(self, symbol: str, current_price: float) -> Optional[float]:
        """
        Calculate unrealized P&L percentage

        Args:
            symbol: Trading symbol
            current_price: Current market price

        Returns:
            P&L percentage or None if no position
        """
        position = self.positions.get(symbol)
        if not position:
            return None

        avg_price = position["avg_price"]
        pnl_pct = (current_price - avg_price) / avg_price

        return pnl_pct

    def set_stop_loss(self, symbol: str, stop_price: float):
        """
        Set stop-loss level for position

        Args:
            symbol: Trading symbol
            stop_price: Stop-loss price
        """
        self.stop_loss_levels[symbol] = stop_price
        print(f"📌 Stop-loss set for {symbol} at ${stop_price:.2f}")

    def check_stop_loss(self, symbol: str, current_price: float) -> bool:
        """
        Check if stop-loss is triggered

        Args:
            symbol: Trading symbol
            current_price: Current market price

        Returns:
            True if stop-loss triggered
        """
        stop_price = self.stop_loss_levels.get(symbol)
        if stop_price is None:
            return False

        if current_price <= stop_price:
            print(f"🛑 Stop-loss triggered for {symbol}: ${current_price:.2f} <= ${stop_price:.2f}")
            return True

        return False

    def get_portfolio_exposure(self, prices: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate portfolio exposure metrics

        Args:
            prices: Dictionary of current prices {symbol: price}

        Returns:
            Exposure metrics dictionary
        """
        total_value = 0.0
        position_values = {}

        for symbol, position in self.positions.items():
            quantity = position["quantity"]
            price = prices.get(symbol, position.get("current_price", 0))
            value = quantity * price
            position_values[symbol] = value
            total_value += value

        # Calculate concentrations
        concentrations = {}
        if total_value > 0:
            for symbol, value in position_values.items():
                concentrations[symbol] = value / total_value

        return {
            "total_value": total_value,
            "position_values": position_values,
            "concentrations": concentrations,
            "num_positions": len(self.positions),
        }

    def _log_position_update(self, symbol: str, closed: bool = False):
        """Log position update"""
        log_file = self.log_path / f"positions_{datetime.now().date()}.jsonl"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol,
            "closed": closed,
            "position": self.positions.get(symbol) if not closed else None,
        }

        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def get_summary(self) -> Dict[str, Any]:
        """Get position monitor summary"""
        return {
            "num_positions": len(self.positions),
            "symbols": list(self.positions.keys()),
            "stop_loss_count": len(self.stop_loss_levels),
        }
