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
    figs=[('Figure 8 - Courbes nominales température-temps',fire_plot(t,gas,RESULTS_DIR/'01_courbes_feu.png')),('Figure 9 - Trois coupes de référence',geometry_plot(SECTIONS,RESULTS_DIR/'02_coupes_geometriques.png'))]
    for el,name in ((HANGER,'03_suspentes.png'),(CABLE,'04_cable_principal.png')):
      series={f'{c[0]} - {c[1].code}':c[5].ta for c in calcs if c[4] is el and c[3]==15.}
      figs.append((f'Échauffement - {el.name}',steel_plot(t,series,f'Échauffement - {el.name}',RESULTS_DIR/name)))
    summary=[]
    for fn in CURVES:
      for pos in FIRE_POSITIONS:
       for el in (HANGER,CABLE):
        c=next(c for c in calcs if c[0]==fn and c[1]==pos and c[4] is el)
        row={'Feu':fn,'Position':pos.code,'Coupe':c[2].code,'Élément':el.name}
        for tm in READ_TIMES_MIN:row[f'T à {int(tm)} min (°C)']=f'{c[5].ta[np.argmin(abs(t-tm))]:.1f}'.replace('.',',')
        summary.append(row)
    values=[('Diamètre D',f'{w_el.diameter_m:.3f} m'),('Fraction exposée ηexp',f'{w_el.exposed_fraction:.3f}'),('Aire A',f'{area(w_el.diameter_m):.6f} m²'),('Périmètre Am',f'{perimeter(w_el.diameter_m):.6f} m'),('Facteur Am/V',f'{w_amv:.3f} m⁻¹'),('Distance 3D',f'{w_dist:.3f} m'),('Température des gaz θg',f'{w_h.tg[idx]:.2f} °C'),('Température acier θa,t',f'{w_h.ta[idx-1]:.2f} °C'),('αc',f'{ALPHA_C:.1f} W/m²K'),('Φ',f'{PHI:.3f}'),('εm',f'{EPSILON_M:.3f}'),('εf',f'{EPSILON_F:.3f}'),('ca',f'{w_h.cp[idx]:.1f} J/kgK'),('ρa',f'{RHO_STEEL:.1f} kg/m³'),('Δt',f'{DT_SECONDS:.1f} s')]
    case={'fire':w_fn,'position':w_pos.label,'section':w_sec.code,'element':w_el.name,'fire_length':w_L,'values':values,'qc':w_h.qc[idx],'qr':w_h.qr[idx],'qn':w_h.qn[idx],'dta':w_h.dta[idx],'ta0':w_h.ta[idx-1],'ta1':w_h.ta[idx]}
    if VERBOSE:print('Cas critique à 30 min:',w_fn,w_pos.code,w_sec.code,w_el.name,f'{w_h.ta[idx]:.2f} °C')
    if GENERATE_REPORT:print(build(RESULTS_DIR/REPORT_FILENAME,figs,summary,case,ASSETS_DIR,SECTIONS))
    if SHOW_PLOTS:
      for _,pth in figs:
       im=plt.imread(pth);fig,ax=plt.subplots(figsize=(10,6));ax.imshow(im);ax.axis('off')
      plt.show()
if __name__=='__main__':run()
