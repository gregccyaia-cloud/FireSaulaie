import numpy as np,matplotlib.pyplot as plt
from config import *
from fire import CURVES
from geometry import area,perimeter,section_factor,nearest_section,receiver_xyz,distance3d
from thermal import integrate
from plotting import fire_plot,steel_plot,geometry_plot,integration_plot
from report import build
def run():
 RESULTS_DIR.mkdir(exist_ok=True);t=np.arange(0,T_MAX_MIN+DT_SECONDS/60,DT_SECONDS/60);gas={n:f(t) for n,f in CURVES.items()};calc=[]
 for fn,tg in gas.items():
  for pos in FIRE_POSITIONS:
   sec=nearest_section(pos,SECTIONS)
   for L in FIRE_LENGTHS_M:
    for el in (HANGER,CABLE):
     amv=section_factor(el.diameter_m,el.exposed_fraction);h=integrate(t,tg,amv);dist=distance3d((pos.x_m,0,TRUCK_HEIGHT_M),receiver_xyz(sec,el.name));calc.append((fn,pos,sec,L,el,h,dist,amv))
 idx=np.argmin(abs(t-30));fn,pos,sec,L,el,h,dist,amv=max(calc,key=lambda c:c[5].ta[idx])
 fire_fig=fire_plot(t,gas,RESULTS_DIR/'01_courbes_feu.png');geom_fig=geometry_plot(SECTIONS,RESULTS_DIR/'02_coupes.png');integ_fig=integration_plot(h,30.,RESULTS_DIR/'A_01_integration.png')
 figures=[]
 for e,file,no in ((HANGER,'03_suspente.png',10),(CABLE,'04_cable.png',11)):
  series=[(f'{c[0]} - {c[1].code}',c[5].ta,c[1].code,c[3]) for c in calc if c[4] is e and c[3]==15.];figures.append((f'Figure {no} - Échauffement - {e.name} - foyer 15 m',steel_plot(t,series,f'Échauffement - {e.name}',RESULTS_DIR/file)))
 appendix=[];no=12
 for fire in CURVES:
  for e in (HANGER,CABLE):
   series=[(f'{c[1].code} - L={int(c[3])} m',c[5].ta,c[1].code,c[3]) for c in calc if c[0]==fire and c[4] is e];appendix.append((f'Figure B.{no-11} - {fire} - {e.name} - tous les cas',steel_plot(t,series,f'{fire} - {e.name} - tous les cas',RESULTS_DIR/f'B_{no}.png')));no+=1
 summary=[]
 for fire in CURVES:
  for p in FIRE_POSITIONS:
   for e in (HANGER,CABLE):
    c=next(c for c in calc if c[0]==fire and c[1]==p and c[4] is e);row={'Feu':fire,'Position':p.code,'Coupe':c[2].code,'Élément':e.name}
    for tm in READ_TIMES_MIN:row[f'T à {int(tm)} min (°C)']=f'{c[5].ta[np.argmin(abs(t-tm))]:.1f}'.replace('.',',')
    summary.append(row)
 vals=[('Diamètre D',f'{el.diameter_m:.3f} m'),('Fraction exposée ηexp',f'{el.exposed_fraction:.3f}'),('Aire A',f'{area(el.diameter_m):.6f} m²'),('Périmètre A_m',f'{perimeter(el.diameter_m):.6f} m'),('Facteur A_m/V',f'{amv:.3f} m⁻¹'),('Distance 3D',f'{dist:.3f} m'),('Température gaz θ_g',f'{h.tg[idx]:.2f} °C'),('Température acier θ_a,t',f'{h.ta[idx-1]:.2f} °C'),('α_c',f'{ALPHA_C:.1f} W/m²K'),('Φ',f'{PHI:.3f}'),('ε_m',f'{EPSILON_M:.3f}'),('ε_f',f'{EPSILON_F:.3f}'),('c_a',f'{h.cp[idx]:.1f} J/kgK'),('ρ_a',f'{RHO_STEEL:.1f} kg/m³'),('Δt',f'{DT_SECONDS:.1f} s')]
 case={'fire':fn,'position':pos.label,'section':sec.code,'element':el.name,'L':L,'values':vals,'qc':h.qc[idx],'qr':h.qr[idx],'qn':h.qn[idx],'dta':h.dta[idx],'ta0':h.ta[idx-1],'ta1':h.ta[idx]}
 params=[('Dimensions du poids lourd (hypothèse géométrique V1.5_A)',f'{TRUCK_LENGTH_M:.1f} × {TRUCK_WIDTH_M:.2f} × {TRUCK_HEIGHT_M:.2f} m'),('Longueurs de foyer (analyse paramétrique)','10 m ; 15 m ; 20 m'),('Positions de feu (géométrie du projet)','F1 ouest ; F2 centrale ; F3 est'),('Durée du calcul (hypothèse d’étude)','120 min'),('Pas de temps Δt (NF EN 1993-1-2, § 4.2.5.1)',f'{DT_SECONDS:.1f} s'),('Facteur de configuration Φ (NF EN 1991-1-2, § 3.1)',f'{PHI:.2f}'),('Facteur d’ombre k_sh (NF EN 1993-1-2, § 4.2.5.1)',f'{K_SH:.2f}'),('Coefficient convectif α_c (NF EN 1991-1-2, § 3.1)',f'{ALPHA_C:.1f} W/m²K'),('Émissivité acier ε_m (NF EN 1993-1-2, § 4.2.5.1)',f'{EPSILON_M:.2f}'),('Émissivité du feu ε_f (NF EN 1993-1-2, § 4.2.5.1)',f'{EPSILON_F:.2f}'),('Masse volumique ρ_a (NF EN 1993-1-2, § 3.4.1)',f'{RHO_STEEL:.0f} kg/m³'),('Chaleur spécifique c_a(θ_a) (NF EN 1993-1-2, § 3.4.1.2)','Loi par morceaux mise à jour à chaque pas')]
 if VERBOSE:print('Cas critique à 30 min:',fn,pos.code,sec.code,el.name,f'{h.ta[idx]:.2f} °C')
 if GENERATE_REPORT:print('[OK]',build(RESULTS_DIR/REPORT_FILENAME,ASSETS_DIR,SECTIONS,params,summary,figures,case,appendix,integ_fig,fire_fig,geom_fig))
 if SHOW_PLOTS:
  for p in [fire_fig,geom_fig,integ_fig]+[x[1] for x in figures+appendix]:
   im=plt.imread(p);fig,ax=plt.subplots();ax.imshow(im);ax.axis('off')
  plt.show()
if __name__=='__main__':run()
