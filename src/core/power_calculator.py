"""
Power/Torque Calculator for Assetto Corsa cars.

Computes real-time power (HP) and torque (Nm) curves from power.lut data
and turbo multiplier parameters from engine.ini.

Physics:
    Torque (Nm) = Power (HP) × 745.7 / (RPM × 2π / 60)
    With turbo:  Effective_HP = Base_HP × (1 + boost)
    Boost at RPM = MAX_BOOST × clamp((RPM / REFERENCE_RPM), 0, 1) ^ GAMMA
"""

import math
from typing import List, Tuple, Optional, Dict


class PowerTorqueCalculator:
    """Calculate power and torque curves from LUT data and turbo config."""

    HP_TO_WATTS = 745.7  # 1 HP = 745.7 W

    def __init__(self, power_points: List[Tuple[float, float]],
                 turbo_configs: Optional[List[Dict]] = None):
        """
        Args:
            power_points: List of (RPM, HP) tuples from power.lut
            turbo_configs: List of turbo config dicts, each with keys:
                           max_boost, wastegate, reference_rpm, gamma
        """
        self.power_points = sorted(power_points, key=lambda p: p[0])
        self.turbo_configs = turbo_configs or []

    @staticmethod
    def hp_to_torque_nm(hp: float, rpm: float) -> float:
        """Convert HP to torque in Nm at a given RPM.

        Formula: Torque = HP × 745.7 / (RPM × 2π / 60)
                        = HP × 745.7 × 60 / (RPM × 2π)
                        = HP × 7120.82 / RPM   (approx)
        """
        if rpm <= 0:
            return 0.0
        return hp * PowerTorqueCalculator.HP_TO_WATTS / (rpm * 2.0 * math.pi / 60.0)

    def interpolate_power(self, rpm: float) -> float:
        """Linearly interpolate base HP from the power curve at a given RPM."""
        pts = self.power_points
        if not pts:
            return 0.0
        if rpm <= pts[0][0]:
            return pts[0][1]
        if rpm >= pts[-1][0]:
            return pts[-1][1]
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            if x1 <= rpm <= x2:
                t = (rpm - x1) / (x2 - x1)
                return y1 + t * (y2 - y1)
        return 0.0

    def boost_at_rpm(self, rpm: float) -> float:
        """Total boost pressure (bar) from all turbo units at a given RPM.

        Each turbo contributes:
            boost_i = MAX_BOOST × clamp(RPM / REFERENCE_RPM, 0, 1) ^ GAMMA
        The effective boost is the sum (multi-turbo setups add up).
        """
        total = 0.0
        for tc in self.turbo_configs:
            max_boost = tc.get('max_boost', 0.0)
            ref_rpm = tc.get('reference_rpm', 3000)
            gamma = tc.get('gamma', 2.5)
            if ref_rpm <= 0:
                continue
            ratio = min(rpm / ref_rpm, 1.0)
            ratio = max(ratio, 0.0)
            total += max_boost * (ratio ** gamma)
        return total

    def effective_power(self, rpm: float) -> float:
        """HP after applying turbo boost: base_HP × (1 + boost)."""
        base = self.interpolate_power(rpm)
        boost = self.boost_at_rpm(rpm)
        return base * (1.0 + boost)

    def compute_curves(self, rpm_step: float = 100.0) -> Dict:
        """Compute full power and torque curves.

        Returns:
            dict with keys:
              rpm_values     – list of RPM sample points
              base_hp        – base HP at each RPM (no turbo)
              base_torque    – base torque Nm at each RPM
              effective_hp   – HP with turbo boost
              effective_torque – torque Nm with turbo boost
              boost_curve    – boost bar at each RPM
              peak_base_hp   – (rpm, hp)
              peak_base_torque – (rpm, Nm)
              peak_eff_hp    – (rpm, hp)
              peak_eff_torque – (rpm, Nm)
        """
        if not self.power_points:
            return self._empty_result()

        min_rpm = self.power_points[0][0]
        max_rpm = self.power_points[-1][0]

        rpm_values = []
        r = min_rpm
        while r <= max_rpm:
            rpm_values.append(r)
            r += rpm_step
        if rpm_values and rpm_values[-1] < max_rpm:
            rpm_values.append(max_rpm)

        base_hp = []
        base_torque = []
        eff_hp = []
        eff_torque = []
        boost_curve = []

        peak_bhp = (0, 0.0)
        peak_btq = (0, 0.0)
        peak_ehp = (0, 0.0)
        peak_etq = (0, 0.0)

        for rpm in rpm_values:
            bh = self.interpolate_power(rpm)
            bt = self.hp_to_torque_nm(bh, rpm)
            eh = self.effective_power(rpm)
            et = self.hp_to_torque_nm(eh, rpm)
            b = self.boost_at_rpm(rpm)

            base_hp.append(bh)
            base_torque.append(bt)
            eff_hp.append(eh)
            eff_torque.append(et)
            boost_curve.append(b)

            if bh > peak_bhp[1]:
                peak_bhp = (rpm, bh)
            if bt > peak_btq[1]:
                peak_btq = (rpm, bt)
            if eh > peak_ehp[1]:
                peak_ehp = (rpm, eh)
            if et > peak_etq[1]:
                peak_etq = (rpm, et)

        return {
            'rpm_values': rpm_values,
            'base_hp': base_hp,
            'base_torque': base_torque,
            'effective_hp': eff_hp,
            'effective_torque': eff_torque,
            'boost_curve': boost_curve,
            'peak_base_hp': peak_bhp,
            'peak_base_torque': peak_btq,
            'peak_eff_hp': peak_ehp,
            'peak_eff_torque': peak_etq,
        }

    @staticmethod
    def _empty_result() -> Dict:
        return {
            'rpm_values': [],
            'base_hp': [], 'base_torque': [],
            'effective_hp': [], 'effective_torque': [],
            'boost_curve': [],
            'peak_base_hp': (0, 0.0), 'peak_base_torque': (0, 0.0),
            'peak_eff_hp': (0, 0.0), 'peak_eff_torque': (0, 0.0),
        }
