from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class LongitudinalStation:
    code: str
    x_m: float
    deck_low_clearance_m: float
    main_cable_axis_height_m: float

STATIONS: Tuple[LongitudinalStation, ...] = (
    LongitudinalStation("WEST", 0.0, 6.125, 8.120),
    LongitudinalStation("M7_AXIS", 14.0, 6.900, 9.400),
    LongitudinalStation("EAST", 27.0, 7.250, 11.070),
)

@dataclass(frozen=True)
class BridgeGeometry:
    deck_total_width_m: float = 7.40
    half_width_m: float = 3.70
    profile_break_y_m: float = 1.91
    profile_break_rise_m: float = 0.19
    edge_rise_m: float = 0.61
    hanger_lower_axis_above_low_point_m: float = 0.82
    hanger_diameter_m: float = 0.042
    hanger_spacing_m: float = 6.25
    main_cable_diameter_m: float = 0.132

@dataclass(frozen=True)
class RoadGeometry:
    west_carriageway_width_m: float = 13.0
    median_width_m: float = 2.0
    east_carriageway_width_m: float = 12.0

@dataclass(frozen=True)
class TruckPosition:
    code: str
    label: str
    x_m: float

# Provisional representative positions along the crossing.
# Edit x_m when lane axes are fixed from the road survey.
TRUCK_POSITIONS: Tuple[TruckPosition, ...] = (
    TruckPosition("F1", "Zone ouest", 3.25),
    TruckPosition("F2", "Axe M7", 14.00),
    TruckPosition("F3", "Zone est", 24.00),
)
