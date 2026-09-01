from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PNG_DIR=ROOT/'results'/'png'; CSV_DIR=ROOT/'results'/'csv'; REPORT_DIR=ROOT/'results'/'reports'; LOG_DIR=ROOT/'logs'
SIM_DURATION_MIN=120.; TIME_STEP_SEC=5.; READ_TIMES_MIN=(15,30,60,90,120); THRESHOLDS_C=(400,500,600,700)
VERBOSE=True; SAVE_PNG=True; SHOW_PLOTS=False; GENERATE_REPORT=True
FLAME_HEIGHTS_M=(10.,12.,15.)
T0_C=20.; RHO_STEEL=7850.; EPS_STEEL=.7; EPS_FIRE=1.; ALPHA_C_DIRECT=25.; SIGMA=5.670374419e-8
# Coefficients de depistage V1.2, a ne pas confondre avec un modele de feu localise normatif.
EXPOSURE={'deck':(1.,1.),'hanger_direct':(.85,.85),'hanger_masked':(.35,.25),'cable_direct':(.60,.60),'cable_masked':(.20,.15)}
DECK_SECTION_FACTOR_M_1=100. # provisoire, a remplacer par geometrie thermique du caisson
REPORT_NAME='Rapport_V1_2_Consolide.docx'
