from dataclasses import dataclass
@dataclass(frozen=True)
class Position: code:str; label:str; x_m:float
POSITIONS=(Position('F1','Zone ouest',3.25),Position('F2','Axe M7',14.),Position('F3','Zone est',24.))
X_STATIONS=(0.,14.,27.); H_DECK=(6.125,6.900,7.250); H_CABLE=(8.120,9.400,11.070)
DECK_WIDTH_M=7.40; DECK_HALF_WIDTH_M=3.70; PROFILE_BREAK_Y_M=1.91; PROFILE_BREAK_RISE_M=.19; EDGE_RISE_M=.61
HANGER_LOWER_DZ_M=.82; HANGER_DIAMETER_M=.042; HANGER_SPACING_M=6.25; CABLE_DIAMETER_M=.132
M7_WEST_M=13.; M7_MEDIAN_M=2.; M7_EAST_M=12.; TRUCK_L_M=16.; TRUCK_W_M=2.5; TRUCK_H_M=4.
