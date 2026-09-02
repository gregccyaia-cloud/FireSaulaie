from pathlib import Path
ROOT=Path(__file__).resolve().parent;ASSETS=ROOT/'assets';PNG=ROOT/'results/png';REPORTS=ROOT/'results/reports'
TMAX=120.;DT=5.;TIMES=(15,30,60,90,120);FLAME_HEIGHTS=(10.,15.,20.)
T0=20.;RHO=7850.;EPSM=.7;EPSF=1.;SIGMA=5.67e-8;ALPHA=25.;KSH=1.
E_CABLE=160.;N_CABLE=3300.;FTRD_CABLE=11897.;E_HANGER=205.;N_HANGER=115.;FTRD_HANGER=541.
REPORT='Rapport_incendie_V2_2.docx'
