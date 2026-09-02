import numpy as np,pandas as pd
from config import *
from model import gas,solve,phi,ky,ke
from plots import fireplot,geom,family,ratio_plot,envelope
from report import build
POS=[{'code':'F1','deck':6.125,'hanger':6.945,'cable':8.120},{'code':'F2','deck':6.900,'hanger':7.720,'cable':9.400},{'code':'F3','deck':7.250,'hanger':8.070,'cable':11.070}]
def main():
 for d in (PNG,DATA,REPORTS):d.mkdir(parents=True,exist_ok=True)
 ts=np.arange(0,TMAX*60+DT,DT);tm=ts/60;names=('ISO 834','Feu extérieur','HC');curves={f:gas(tm,f) for f in names};cases=[]
 for fn,tg in curves.items():
  for p in POS:
   for L in LENGTHS:cases.append({'fire':fn,'pos':p['code'],'L':L,'tm':tm,'hanger':solve(ts,tg,.042,phi(L,p['hanger'])),'cable':solve(ts,tg,.132,phi(L,p['cable']))})
 firep=PNG/'feux.png';geomp=PNG/'geometrie.png';fireplot(tm,curves,firep);geom(POS,geomp);f12=PNG/'fig12.png';f13=PNG/'fig13.png';family(cases,'hanger',20,f12,'Suspente secondaire - foyer 20 m');family(cases,'cable',20,f13,'Câble principal - foyer 20 m')
 rows=[];maxlines=[]
 for fn in names:
  sel=[c for c in cases if c['fire']==fn]
  for el,label,E,N,F in [('hanger','Suspente secondaire',E_HANGER,N_HANGER,FTRD_HANGER),('cable','Câble principal clos',E_CABLE,N_CABLE,FTRD_CABLE)]:
   env=np.max(np.vstack([c[el] for c in sel]),axis=0);ratio=N/(ky(env)*F);ok=np.where(ratio<=1)[0];tmax=tm[ok[-1]] if len(ok) else 0;maxlines.append(f'{label} - {fn} : {tmax:.1f} min')
   for t in TIMES:
    i=np.argmin(abs(tm-t));T=env[i];rd=float(ky(T)*F);eta=N/rd if rd else np.inf;rows.append([fn,t,label,round(T,1),round(float(ky(T)),3),round(float(ke(T)*E),1),round(rd,1),round(eta,3),'Justifié' if eta<=1 else 'Non justifié'])
 struct=pd.DataFrame(rows,columns=['Feu','t (min)','Organe','θ (°C)','ky,θ','Eθ (GPa)','Ft,Rd,θ (kN)','ηfi','Statut']);f14=PNG/'fig14.png';f15=PNG/'fig15.png';ratio_plot(struct,'Suspente secondaire',f14,'Ratio ηfi - Suspente secondaire');ratio_plot(struct,'Câble principal clos',f15,'Ratio ηfi - Câble principal clos')
 temps=pd.DataFrame([[t,*[round(max(c[e][np.argmin(abs(tm-t))] for c in cases),1) for e in ('hanger','cable')]] for t in TIMES],columns=['Temps (min)','Suspente (°C)','Câble principal (°C)'])
 annex=[]
 for fn in names:
  for el,lab in [('hanger','Suspente secondaire'),('cable','Câble principal clos')]:p=PNG/f'B_{fn}_{el}.png';envelope(cases,fn,el,p,f'{fn} - {lab}');annex.append((p,f'{fn} - {lab} : cas et enveloppe maximale.'))
 ctx={'assets':[(ASSETS/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.',16),(ASSETS/'ZZ extrait plan suspension.png','Figure 2 - Système de suspension.',16),(ASSETS/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale.',16),(ASSETS/'ZZ coupe transv.png','Figure 4 - Coupe transversale.',16)],'cerema':ASSETS/'extrait_cerema_choix_courbes.png','fire':firep,'geom':geomp,'intrados':ASSETS/'ZZ_approxim intrados demi-coupe.png','f12':f12,'f13':f13,'f14':f14,'f15':f15,'annex':annex,'temps':temps,'struct':struct,'maxtext':'Temps maximal justifié, au pas de 5 s : '+' ; '.join(maxlines)+'.','geomtab':pd.DataFrame([[p['code'],p['deck'],p['hanger'],p['cable']] for p in POS],columns=['Coupe','Intrados','Suspente','Câble']),'params':pd.DataFrame([['Ft,Rd câble principal (cf. SAU_AVP_NDC_062_A_JustifOADéfi)','11 897 kN'],['NQP câble principal','3 300 kN'],['E câble principal','160 GPa'],['Ft,Rd suspente secondaire (cf. SAU_AVP_NDC_062_A_JustifOADéfi)','541 kN'],['NQP suspente secondaire','115 kN'],['E suspente secondaire','205 GPa']],columns=['Paramètre','Valeur'])}
 print(build(ctx,REPORTS/REPORT))
if __name__=='__main__':main()
