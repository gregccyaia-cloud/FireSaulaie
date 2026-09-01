from dataclasses import dataclass
@dataclass(frozen=True)
class Position: code:str;label:str;x_m:float
POSITIONS=(Position('F1','Zone ouest',3.25),Position('F2','Axe M7',14.),Position('F3','Zone est',24.))
X=(0.,14.,27.);H_DECK=(6.125,6.900,7.250);H_CABLE=(8.120,9.400,11.070)
DECK_WIDTH=7.40;HALF_WIDTH=3.70;BREAK_Y=1.91;BREAK_DZ=.19;EDGE_DZ=.61
HANGER_DZ=.82;HANGER_D=.042;HANGER_SPACING=6.25;CABLE_D=.132
ROAD=(13.,2.,12.);TRUCK=(16.,2.5,4.)
