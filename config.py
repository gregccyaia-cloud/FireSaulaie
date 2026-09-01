from dataclasses import dataclass
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent
ASSETS_DIR=BASE_DIR/'assets'; RESULTS_DIR=BASE_DIR/'results'
SHOW_PLOTS=False; GENERATE_REPORT=True; VERBOSE=True
REPORT_FILENAME='Rapport_incendie_V1_4.docx'
T_MAX_MIN=120.; DT_SECONDS=5.; READ_TIMES_MIN=(15.,30.,60.,90.,120.)
AMBIENT_TEMPERATURE_C=20.; ALPHA_C=25.; EPSILON_M=.7; EPSILON_F=1.; PHI=1.; K_SH=1.
SIGMA=5.67e-8; RHO_STEEL=7850.
FIRE_LENGTHS_M=(10.,15.,20.)
TRUCK_HEIGHT_M=4.
@dataclass(frozen=True)
class CircularElement:
    name:str; diameter_m:float; exposed_fraction:float=1.
CABLE=CircularElement('Câble principal clos',.132)
HANGER=CircularElement('Suspente secondaire',.042)
@dataclass(frozen=True)
class Section:
    code:str; label:str; x_m:float; intrados_m:float; cable_m:float
SECTIONS=(Section('OUEST','Bord ouest circulable',0.,6.125,8.12),Section('AXE','Axe M7',14.,6.90,9.40),Section('EST','Bord est circulable',27.,7.25,11.07))
@dataclass(frozen=True)
class FirePosition:
    code:str; label:str; x_m:float
FIRE_POSITIONS=(FirePosition('F1','Position ouest',4.5),FirePosition('F2','Position centrale',13.5),FirePosition('F3','Position est',22.5))
DECK_HALF_WIDTH_M=3.70; HANGER_LOWER_OFFSET_M=.82
