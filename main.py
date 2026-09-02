import numpy as np
from config import *
from fire import CURVES
from geometry import section_factor,nearest_section,receiver_xyz,distance3d
from thermal import integrate
from structural import ft_theta
from plotting import fire_plot,grouped,envelope,geom,integration_pair
from report import build
def run():
 RESULTS_DIR.mkdir(exist_ok=True);t=np.arange(0,T_MAX_MIN+DT_SECONDS/60,DT_SECONDS/60);gas={n:f(t) for n,f in CURVES.items()};C=[]
 for fn,tg in gas.items():
  for p in FIRE_POSITIONS:
   s=nearest_section(p,SECTIONS)
   for L in FIRE_LENGTHS_M:
    for e in (HANGER,MAIN_CABLE):C.append((fn,p,s,L,e,integrate(t,tg,section_factor(e.diameter_m)),distance3d((p.x_m,0,TRUCK_HEIGHT_M),receiver_xyz(s,e.name))))
 i=np.argmin(abs(t-30));fn,p,s,L,e,h,dist=max(C,key=lambda c:c[5].ta[i]);hs=next(c[5] for c in C if c[0]==fn and c[1]==p and c[3]==L and c[4] is HANGER);hp=next(c[5] for c in C if c[0]==fn and c[1]==p and c[3]==L and c[4] is MAIN_CABLE)
 ff=fire_plot(t,gas,RESULTS_DIR/'01_feux.png');gf=geom(SECTIONS,RESULTS_DIR/'02_geom.png');integ=integration_pair(hs,hp,RESULTS_DIR/'A_integration.png')
 figs=[];rfigs=[]
 for el,no in ((HANGER,12),(MAIN_CABLE,13)):
  z=[(c[0],c[1].code,c[5].ta) for c in C if c[4] is el and c[3]==15.];figs.append((f'Figure {no} - Température - {el.name}',grouped(t,z,f'Température - {el.name}','Température acier (°C)',RESULTS_DIR/f'T{no}.png')))
  z=[(c[0],c[1].code,ft_theta(el.ft_rd_20_kn,c[5].ta)) for c in C if c[4] is el and c[3]==15.];rfigs.append((f'Figure {no+2} - Résistance indicative - {el.name}',grouped(t,z,f'Résistance - {el.name}','Fₜ,Rd,θ (kN)',RESULTS_DIR/f'R{no}.png')))
 summary=[];rs=[]
 for fire in CURVES:
  for pp in FIRE_POSITIONS:
   for el in (HANGER,MAIN_CABLE):
    c=next(c for c in C if c[0]==fire and c[1]==pp and c[3]==15. and c[4] is el);a={'Feu':fire,'Position':pp.code,'Élément':el.name};b={'Feu':fire,'Position':pp.code,'Élément':el.name,'Fₜ,Rd,20':f'{el.ft_rd_20_kn:.0f}'}
    for tm in READ_TIMES_MIN:j=np.argmin(abs(t-tm));a[f'T {int(tm)} min']=f'{c[5].ta[j]:.1f}';b[f'Fₜ,Rd,θ {int(tm)} min']=f'{float(ft_theta(el.ft_rd_20_kn,c[5].ta[j])):.0f}'
    summary.append(a);rs.append(b)
 appendix=[];k=1
 for el in (HANGER,MAIN_CABLE):
  z=[(c[0],c[1].code,c[3],c[5].ta) for c in C if c[4] is el];appendix.append((f'Figure B.{k} - Température, 3 feux - {el.name}',envelope(t,z,f'Températures et enveloppes - {el.name}','Température (°C)',RESULTS_DIR/f'B{k}.png')));k+=1
  z=[(c[0],c[1].code,c[3],ft_theta(el.ft_rd_20_kn,c[5].ta)) for c in C if c[4] is el];appendix.append((f'Figure B.{k} - Résistance, 3 feux - {el.name}',envelope(t,z,f'Résistances et enveloppes - {el.name}','Fₜ,Rd,θ (kN)',RESULTS_DIR/f'B{k}.png')));k+=1
 vals=[('Élément critique',e.name),('Fₜ,Rd,20',f'{e.ft_rd_20_kn:.0f} kN'),('A_m/V',f'{section_factor(e.diameter_m):.3f} m⁻¹'),('Distance 3D',f'{dist:.3f} m'),('θ_g',f'{h.tg[i]:.2f} °C'),('θ_a,i',f'{h.ta[i-1]:.2f} °C'),('c_a',f'{h.cp[i]:.1f} J/kgK')];case={'fire':fn,'position':p.label,'section':s.code,'L':L,'values':vals,'qc':h.qc[i],'qr':h.qr[i],'qn':h.qn[i],'dta':h.dta[i]}
 params=[('Trois feux','CN - ISO 834 ; extérieur ; HC'),('Styles','pointillé ; plein ; trait mixte'),('Durée','120 min'),('Pas','5 s'),('Φ','1,0'),('Fₜ,Rd,20 câble','11 897 kN'),('Fₜ,Rd,20 suspente','541 kN')]
 print(build(RESULTS_DIR/REPORT_FILENAME,ASSETS_DIR,SECTIONS,params,summary,rs,figs,rfigs,case,appendix,integ,ff,gf))
if __name__=='__main__':run()
