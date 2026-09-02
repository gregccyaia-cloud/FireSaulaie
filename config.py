from dataclasses import dataclass
from pathlib import Path
ROOT=Path(__file__).resolve().parent; ASSETS_DIR=ROOT/'assets'; RESULTS_DIR=ROOT/'results'
REPORT_FILENAME='Rapport_incendie_V2_0.docx'; SHOW_PLOTS=False; GENERATE_REPORT=True
T_MAX_MIN=120.; DT_SECONDS=5.; READ_TIMES_MIN=(15.,30.,60.,90.,120.)
AMBIENT_C=20.; ALPHA_C=25.; EPSILON_M=.70; EPSILON_F=1.; PHI=1.; K_SH=1.; SIGMA=5.67e-8; RHO_STEEL=7850.
TRUCK_LENGTH_M=16.; TRUCK_WIDTH_M=2.5; TRUCK_HEIGHT_M=4.; FIRE_LENGTHS_M=(10.,15.,20.)
@dataclass(frozen=True)
class Element: name:str; diameter_m:float; ft_rd_20_kn:float
HANGER=Element('Suspente secondaire',.042,541.); MAIN_CABLE=Element('Suspension principale - câble clos',.132,11897.)
@dataclass(frozen=True)
class Section: code:str; label:str; x_m:float; intrados_m:float; cable_m:float
SECTIONS=(Section('OUEST','Bord ouest circulable',0.,6.125,8.12),Section('AXE','Axe de la M7',14.,6.90,9.40),Section('EST','Bord est circulable',27.,7.25,11.07))
@dataclass(frozen=True)
class FirePosition: code:str; label:str; x_m:float
FIRE_POSITIONS=(FirePosition('F1','Position ouest',4.5),FirePosition('F2','Position centrale',13.5),FirePosition('F3','Position est',22.5))
DECK_HALF_WIDTH_M=3.70; HANGER_LOWER_OFFSET_M=.82
