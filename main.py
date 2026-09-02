import numpy as np
from config import *
from fire import CURVES
from geometry import area,perimeter,section_factor,nearest_section,receiver_xyz,distance3d
from thermal import integrate
from structural import ft_theta
from plotting import fire_plot,curves,geom,integration
from report import build
def run():
 RESULTS_DIR.mkdir(exist_ok=True);t=np.arange(0,T_MAX_MIN+DT_SECONDS/60,DT_SECONDS/60);gas={n:f(t) for n,f in CURVES.items()};C=[]
 for fn,tg in gas.items():
  for pos in FIRE_POSITIONS:
   sec=nearest_section(pos,SECTIONS)
   for L in FIRE_LENGTHS_M:
    for el in (HANGER,CABLE):
     h=integrate(t,tg,section_factor(el.diameter_m));C.append((fn,pos,sec,L,el,h,distance3d((pos.x_m,0,TRUCK_HEIGHT_M),receiver_xyz(sec,el.name))))
 i=np.argmin(abs(t-30));fn,pos,sec,L,el,h,dist=max(C,key=lambda c:c[5].ta[i]);ff=fire_plot(t,gas,RESULTS_DIR/'01_feu.png');gf=geom(SECTIONS,RESULTS_DIR/'02_geom.png');integ=integration(h,RESULTS_DIR/'A_integr.png')
 figs=[];resfigs=[]
 for e,n in ((HANGER,11),(CABLE,12)):
  s=[(f'{c[0]}-{c[1].code}',c[5].ta,c[1].code,c[3]) for c in C if c[4] is e and c[3]==15.];figs.append((f'Figure {n} - Échauffement - {e.name}',curves(t,s,f'Échauffement - {e.name}',"Température de l'acier (°C)",RESULTS_DIR/f'T_{n}.png')))
  sr=[(f'{c[0]}-{c[1].code}',ft_theta(e.ft_rd_20_kn,c[5].ta),c[1].code,c[3]) for c in C if c[4] is e and c[3]==15.];resfigs.append((f'Figure {n+2} - Résistance indicative - {e.name}',curves(t,sr,f'Résistance indicative - {e.name}','Fₜ,Rd,θ (kN)',RESULTS_DIR/f'R_{n}.png')))
 summary=[];rs=[]
 for fire in CURVES:
  for p in FIRE_POSITIONS:
   for e in (HANGER,CABLE):
    c=next(c for c in C if c[0]==fire and c[1]==p and c[4] is e);row={'Feu':fire,'Position':p.code,'Élément':e.name};rr={'Feu':fire,'Position':p.code,'Élément':e.name,'Fₜ,Rd,20 (kN)':f'{e.ft_rd_20_kn:.0f}'}
    for tm in READ_TIMES_MIN:
     j=np.argmin(abs(t-tm));row[f'T {int(tm)} min (°C)']=f'{c[5].ta[j]:.1f}';rr[f'Fₜ,Rd,θ {int(tm)} min (kN)']=f'{float(ft_theta(e.ft_rd_20_kn,c[5].ta[j])):.0f}'
    summary.append(row);rs.append(rr)
 vals=[('Diamètre',f'{el.diameter_m:.3f} m'),('Fₜ,Rd,20',f'{el.ft_rd_20_kn:.0f} kN'),('Aire géométrique',f'{area(el.diameter_m):.6f} m²'),('A_m/V',f'{section_factor(el.diameter_m):.3f} m⁻¹'),('Distance 3D',f'{dist:.3f} m'),('θ_g',f'{h.tg[i]:.2f} °C'),('θ_a,i',f'{h.ta[i-1]:.2f} °C'),('c_a',f'{h.cp[i]:.1f} J/kgK'),('Δt',f'{DT_SECONDS:.1f} s')];case={'fire':fn,'position':pos.label,'section':sec.code,'element':el.name,'L':L,'values':vals,'qc':h.qc[i],'qr':h.qr[i],'qn':h.qn[i],'dta':h.dta[i],'ta0':h.ta[i-1],'ta1':h.ta[i]}
 appendix=[];k=1
 for fire in CURVES:
  for e in (HANGER,CABLE):
   s=[(f'{c[1].code}-L{int(c[3])}',c[5].ta,c[1].code,c[3]) for c in C if c[0]==fire and c[4] is e];appendix.append((f'Figure B.{k} - {fire} - {e.name}',curves(t,s,f'{fire} - {e.name}','Température (°C)',RESULTS_DIR/f'B{k}.png')));k+=1
 params=[('Dimensions camion','16,0 × 2,50 × 4,00 m'),('Longueurs foyer','10 ; 15 ; 20 m'),('Pas Δt (EN 1993-1-2)','5 s'),('Φ (EN 1991-1-2)','1,0'),('Fₜ,Rd,20 câble','11 897 kN'),('Fₜ,Rd,20 suspente','541 kN')]
 print(build(RESULTS_DIR/REPORT_FILENAME,ASSETS_DIR,SECTIONS,params,summary,rs,figs,resfigs,case,appendix,integ,ff,gf))
if __name__=='__main__':run()
