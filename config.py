from pathlib import Path
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets';PNG=ROOT/'results/png';CSV=ROOT/'results/csv';REPORTS=ROOT/'results/reports'
TMAX=120.;DT=5.;TIMES=(15,30,60,90,120);LENGTHS=(10.,15.,20.)
T0=20.;RHO=7850.;EPSM=.7;EPSF=1.;SIGMA=5.67e-8;ALPHA=25.;KSH=1.
REPORT='Rapport_incendie_V1_5_D.docx'
