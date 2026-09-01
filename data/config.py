from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PNG_DIR=ROOT/'results'/'png';CSV_DIR=ROOT/'results'/'csv';REPORT_DIR=ROOT/'results'/'reports';LOG_DIR=ROOT/'logs'
DURATION_MIN=120.;DT_S=5.;READ_TIMES=(15,30,60,90,120);FLAME_HEIGHTS=(10.,12.,15.)
GENERATE_REPORT=True;SHOW_PLOTS=False;VERBOSE=True;REPORT_FILENAME='Rapport_V1_3_Consolide.docx'
T0=20.;RHO=7850.;EPS_M=.7;EPS_F=1.;SIGMA=5.670374419e-8;ALPHA_C=25.
# Coefficients de dépistage, provisoires. Couple = (rayonnement, convection)
EXPOSURE={'deck':(1.,1.),'hanger_direct':(.85,.85),'hanger_masked':(.35,.25),'cable_direct':(.60,.60),'cable_masked':(.20,.15)}
DECK_AMV=100.0
