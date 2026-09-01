from dataclasses import dataclass
@dataclass(frozen=True)
class Position: code:str;label:str;x:float;h_deck:float;h_hanger:float;h_cable:float
POSITIONS=(Position('F1','ouest',0.,6.125,6.945,8.120),Position('F2','axe M7',14.,6.900,7.720,9.400),Position('F3','est',27.,7.250,8.070,11.070))
HANGER_D=.042;CABLE_D=.132;HANGER_SPACING=6.25;TRUCK=(16.,2.5,4.);DECK_WIDTH=7.40
