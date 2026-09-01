from dataclasses import dataclass
@dataclass(frozen=True)
class Position: code:str; label:str; x:float
POSITIONS=(Position('F1','Zone ouest',3.25),Position('F2','Axe M7',14.),Position('F3','Zone est',24.))
X=(0.,14.,27.); H_DECK=(6.125,6.9,7.25); H_CABLE=(8.12,9.4,11.07)
DECK_WIDTH=7.4; HANGER_D=.042; CABLE_D=.132; HANGER_DZ=.82
