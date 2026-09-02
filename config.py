from pathlib import Path
ROOT=Path(__file__).resolve().parent;ASSETS=ROOT/'assets';PNG=ROOT/'results/png';DATA=ROOT/'results/data';REPORTS=ROOT/'results/reports'
TMAX=120.;DT=5.;TIMES=(15,30,60,90,120);LENGTHS=(10.,15.,20.)
T0=20.;RHO=7850.;EPSM=.7;EPSF=1.;SIGMA=5.67e-8;ALPHA=25.;KSH=1.
REPORT='Rapport_incendie_V1_5_E.docx'
# Données complémentaires fournies
E_CABLE_GPA=160.;NQP_CABLE_KN=3300.;E_HANGER_GPA=205.;NQP_HANGER_KN=115.
# Données requises pour conclure la résistance: à compléter, sans hypothèse implicite
FY_CABLE_MPA=None;FY_HANGER_MPA=None;CABLE_METALLIC_AREA_MM2=None
