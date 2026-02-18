"""
Power/Torque Calculator for Assetto Corsa cars.

Computes real-time power (HP) and torque (Nm) curves from power.lut data
and turbo multiplier parameters from engine.ini.

The power.lut file contains **torque in Nm** mapped to RPM, despite its name.

Physics (from AC documentation §4.2):
    NA engines:    Final_Torque = LUT_value
    Turbo engines: Final_Torque = LUT_value × (1 + Boost_Pressure)
    Power (HP) = Torque(Nm) × RPM × 2π / (60 × 745.7)
    Boost at RPM = MAX_BOOST × clamp((RPM / REFERENCE_RPM), 0, 1) ^ GAMMA
"""

import math
from typing import List, Tuple, Optional, Dict


class PowerTorqueCalculator:
    """Calculate power and torque curves from LUT data and turbo config."""

    HP_TO_WATTS = 745.7  # 1 HP = 745.7 W

    def __init__(self, torque_points: List[Tuple[float, float]],
                 turbo_configs: Optional[List[Dict]] = None):
        """
        Args:
            torque_points: List of (RPM, Nm) tuples from power.lut
            turbo_configs: List of turbo config dicts, each with keys:
                           max_boost, wastegate, reference_rpm, gamma
        """
        self.torque_points = sorted(torque_points, key=lambda p: p[0])
        self.turbo_configs = turbo_configs or []

    @staticmethod
    def torque_to_hp(torque_nm: float, rpm: float) -> float:
        """Convert torque in Nm to HP at a given RPM.

        Formula: HP = Torque(Nm) × RPM × 2π / (60 × 745.7)
        """
        if rpm <= 0:
            return 0.0
        return torque_nm * rpm * 2.0 * math.pi / (60.0 * PowerTorqueCalculator.HP_TO_WATTS)

    def interpolate_torque(self, rpm: float) -> float:
        """Linearly interpolate base torque (Nm) from the LUT at a given RPM."""
        pts = self.torque_points
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

    def effective_torque(self, rpm: float) -> float:
        """Torque (Nm) after applying turbo boost: base_torque × (1 + boost)."""
        base = self.interpolate_torque(rpm)
        boost = self.boost_at_rpm(rpm)
        return base * (1.0 + boost)

    def compute_curves(self, rpm_step: float = 100.0) -> Dict:
        """Compute full power and torque curves.

        Returns:
            dict with keys:
              rpm_values       – list of RPM sample points
              base_torque      – base torque Nm at each RPM (from LUT)
              base_hp          – base HP at each RPM (derived from torque)
              effective_torque – torque Nm with turbo boost
              effective_hp     – HP with turbo boost (derived from effective torque)
              boost_curve      – boost bar at each RPM
              peak_base_torque – (rpm, Nm)
              peak_base_hp     – (rpm, hp)
              peak_eff_torque  – (rpm, Nm)
              peak_eff_hp      – (rpm, hp)
        """
        if not self.torque_points:
            return self._empty_result()

        min_rpm = self.torque_points[0][0]
        max_rpm = self.torque_points[-1][0]

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
            bt = self.interpolate_torque(rpm)
            bh = self.torque_to_hp(bt, rpm)
            et = self.effective_torque(rpm)
            eh = self.torque_to_hp(et, rpm)
            b = self.boost_at_rpm(rpm)

            base_torque.append(bt)
            base_hp.append(bh)
            eff_torque.append(et)
            eff_hp.append(eh)
            boost_curve.append(b)

            if bt > peak_btq[1]:
                peak_btq = (rpm, bt)
            if bh > peak_bhp[1]:
                peak_bhp = (rpm, bh)
            if et > peak_etq[1]:
                peak_etq = (rpm, et)
            if eh > peak_ehp[1]:
                peak_ehp = (rpm, eh)

        return {
            'rpm_values': rpm_values,
            'base_torque': base_torque,
            'base_hp': base_hp,
            'effective_torque': eff_torque,
            'effective_hp': eff_hp,
            'boost_curve': boost_curve,
            'peak_base_torque': peak_btq,
            'peak_base_hp': peak_bhp,
            'peak_eff_torque': peak_etq,
            'peak_eff_hp': peak_ehp,
        }

    @staticmethod
    def _empty_result() -> Dict:
        return {
            'rpm_values': [],
            'base_torque': [], 'base_hp': [],
            'effective_torque': [], 'effective_hp': [],
            'boost_curve': [],
            'peak_base_torque': (0, 0.0), 'peak_base_hp': (0, 0.0),
            'peak_eff_torque': (0, 0.0), 'peak_eff_hp': (0, 0.0),
        }
