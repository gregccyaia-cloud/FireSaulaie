import numpy as np, matplotlib.pyplot as plt
from config import *
from fire import CURVES
from geometry import area,perimeter,section_factor,nearest_section,receiver_xyz,distance3d
from thermal import integrate
from plotting import fire_plot,steel_plot,geometry_plot
from report import build

def run():
    RESULTS_DIR.mkdir(exist_ok=True);t=np.arange(0,T_MAX_MIN+DT_SECONDS/60,DT_SECONDS/60);gas={n:f(t) for n,f in CURVES.items()};calcs=[]
    for fn,tg in gas.items():
      for pos in FIRE_POSITIONS:
       sec=nearest_section(pos,SECTIONS)
       for L in FIRE_LENGTHS_M:
        for el in (HANGER,CABLE):
         amv=section_factor(el.diameter_m,el.exposed_fraction);h=integrate(t,tg,amv);dist=distance3d((pos.x_m,0,TRUCK_HEIGHT_M),receiver_xyz(sec,el.name));calcs.append((fn,pos,sec,L,el,h,dist,amv))
    idx=np.argmin(abs(t-30));worst=max(calcs,key=lambda c:c[5].ta[idx]);w_fn,w_pos,w_sec,w_L,w_el,w_h,w_dist,w_amv=worst
    figs=[('Figure 8 - Courbes nominales température-temps',fire_plot(t,gas,RESULTS_DIR/'01_courbes_feu.png')),('Figure 9 - Trois coupes géométriques de référence et positions F1, F2 et F3',geometry_plot(SECTIONS,RESULTS_DIR/'02_coupes_geometriques.png'))]
    for el,filename,number in ((HANGER,'03_suspentes.png',10),(CABLE,'04_cable_principal.png',11)):
      series=[]
      for c in calcs:
       if c[4] is el and c[3]==15.:series.append((f"{c[0]} - {c[1].code}",c[5].ta,c[1].code,c[3]))
      figs.append((f'Figure {number} - Échauffement - {el.name} - foyer 15 m',steel_plot(t,series,f'Échauffement - {el.name} - foyer 15 m',RESULTS_DIR/filename,True)))
    appendix=[];num=12
    for fn in CURVES:
      for el in (HANGER,CABLE):
       series=[]
       for c in calcs:
        if c[0]==fn and c[4] is el:series.append((f"{c[1].code} - L={int(c[3])} m",c[5].ta,c[1].code,c[3]))
       appendix.append((f'Figure {num} - {fn} - {el.name} - tous les cas F1/F2/F3 et L=10/15/20 m',steel_plot(t,series,f'{fn} - {el.name} - tous les cas',RESULTS_DIR/f'B_{num}_{fn}_{el.name}.png',True)));num+=1
    summary=[]
    for fn in CURVES:
      for pos in FIRE_POSITIONS:
       for el in (HANGER,CABLE):
        c=next(c for c in calcs if c[0]==fn and c[1]==pos and c[4] is el)
        row={'Feu':fn,'Position':pos.code,'Coupe':c[2].code,'Élément':el.name}
        for tm in READ_TIMES_MIN:row[f'T à {int(tm)} min (°C)']=f'{c[5].ta[np.argmin(abs(t-tm))]:.1f}'.replace('.',',')
        summary.append(row)
    values=[('Diamètre D',f'{w_el.diameter_m:.3f} m'),('Fraction exposée ηexp',f'{w_el.exposed_fraction:.3f}'),('Aire A',f'{area(w_el.diameter_m):.6f} m²'),('Périmètre A_m',f'{perimeter(w_el.diameter_m):.6f} m'),('Facteur A_m/V',f'{w_amv:.3f} m⁻¹'),('Distance 3D',f'{w_dist:.3f} m'),('Température des gaz θ_g',f'{w_h.tg[idx]:.2f} °C'),('Température acier θ_a,t',f'{w_h.ta[idx-1]:.2f} °C'),('α_c',f'{ALPHA_C:.1f} W/m²K'),('Φ',f'{PHI:.3f}'),('ε_m',f'{EPSILON_M:.3f}'),('ε_f',f'{EPSILON_F:.3f}'),('c_a',f'{w_h.cp[idx]:.1f} J/kgK'),('ρ_a',f'{RHO_STEEL:.1f} kg/m³'),('Δt',f'{DT_SECONDS:.1f} s')]
    case={'fire':w_fn,'position':w_pos.label,'section':w_sec.code,'element':w_el.name,'fire_length':w_L,'values':values,'qc':w_h.qc[idx],'qr':w_h.qr[idx],'qn':w_h.qn[idx],'dta':w_h.dta[idx],'ta0':w_h.ta[idx-1],'ta1':w_h.ta[idx]}
    params=[('Dimensions du poids lourd',f'{TRUCK_LENGTH_M:.1f} × {TRUCK_WIDTH_M:.2f} × {TRUCK_HEIGHT_M:.2f} m'),('Longueurs de foyer','10 m ; 15 m ; 20 m'),('Positions de feu','F1 ouest ; F2 centrale ; F3 est'),('Durée du calcul','120 min'),('Pas de temps',f'{DT_SECONDS:.1f} s'),('Facteur de configuration Φ',f'{PHI:.2f}'),('Facteur d’ombre k_sh',f'{K_SH:.2f}'),('Coefficient convectif α_c',f'{ALPHA_C:.1f} W/m²K')]
    if VERBOSE:print('Cas critique à 30 min:',w_fn,w_pos.code,w_sec.code,w_el.name,f'{w_h.ta[idx]:.2f} °C')
    if GENERATE_REPORT:print(build(RESULTS_DIR/REPORT_FILENAME,figs,summary,case,ASSETS_DIR,SECTIONS,params,appendix))
    if SHOW_PLOTS:
      for _,pth in figs+appendix:
       im=plt.imread(pth);fig,ax=plt.subplots(figsize=(10,6));ax.imshow(im);ax.axis('off')
      plt.show()
if __name__=='__main__':run()
