import numpy as np
from data.project_data import STATIONS, BridgeGeometry, TruckPosition

def deck_intrados_rise_m(y_m: float, bridge=BridgeGeometry()) -> float:
    y = abs(float(y_m))
    if y > bridge.half_width_m:
        raise ValueError("Coordonnee y hors tablier")
    if y <= bridge.profile_break_y_m:
        return bridge.profile_break_rise_m / bridge.profile_break_y_m * y
    return bridge.profile_break_rise_m + (bridge.edge_rise_m-bridge.profile_break_rise_m) * (y-bridge.profile_break_y_m)/(bridge.half_width_m-bridge.profile_break_y_m)

def _quadratic_through_stations(x_m: float, field: str) -> float:
    xs=np.array([s.x_m for s in STATIONS], float)
    zs=np.array([getattr(s, field) for s in STATIONS], float)
    return float(np.polyval(np.polyfit(xs, zs, 2), x_m))

def deck_low_clearance_m(x_m: float) -> float:
    # V1.1 smooth interpolation through the three project points.
    return _quadratic_through_stations(x_m, "deck_low_clearance_m")

def main_cable_axis_height_m(x_m: float) -> float:
    # Parabolic approximation through the three values supplied.
    return _quadratic_through_stations(x_m, "main_cable_axis_height_m")

def deck_intrados_height_m(x_m: float, y_m: float=0.0) -> float:
    return deck_low_clearance_m(x_m) + deck_intrados_rise_m(y_m)

def hanger_lower_axis_height_m(x_m: float, bridge=BridgeGeometry()) -> float:
    return deck_low_clearance_m(x_m) + bridge.hanger_lower_axis_above_low_point_m

def geometric_exposure(target_height_m: float, flame_height_m: float, direct_factor: float, masked_factor: float) -> float:
    # Screening rule: inside nominal flame height -> direct factor; above -> masked factor.
    return direct_factor if target_height_m <= flame_height_m else masked_factor

def case_geometry(position: TruckPosition, flame_height_m: float) -> dict:
    x=position.x_m
    h_deck=deck_intrados_height_m(x, 0.0)
    h_hanger=hanger_lower_axis_height_m(x)
    h_cable=main_cable_axis_height_m(x)
    return {"x_m":x, "flame_height_m":flame_height_m, "deck_height_m":h_deck, "hanger_height_m":h_hanger, "cable_height_m":h_cable}
