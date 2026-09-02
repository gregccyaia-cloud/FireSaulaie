import numpy as np,pandas as pd
from config import *
from model import gas,solve,phi,ky,ke
from plots import fireplot,family,envelope
from report import build
POS=[{'code':'F1','deck':6.125,'hanger':6.945,'cable':8.120},{'code':'F2','deck':6.900,'hanger':7.720,'cable':9.400},{'code':'F3','deck':7.250,'hanger':8.070,'cable':11.070}]
def fmt(v):return f'{v:.2f}'.replace('.',',')
def main():
 for d in (PNG,DATA,REPORTS):d.mkdir(parents=True,exist_ok=True)
 ts=np.arange(0,TMAX*60+DT,DT);tm=ts/60;curves={f:gas(tm,f) for f in ('ISO 834','Feu extérieur')};cases=[]
 for fn,tg in curves.items():
  for p in POS:
   for L in LENGTHS:
    Th=solve(ts,tg,.042,phi(L,p['hanger']));Tc=solve(ts,tg,.132,phi(L,p['cable']));cases.append({'fire':fn,'pos':p['code'],'L':L,'tm':tm,'hanger':Th,'cable':Tc})
 firep=PNG/'feu.png';fireplot(tm,curves,firep);f10=PNG/'suspente.png';f11=PNG/'cable.png';family(cases,'hanger',20,f10,'Suspente secondaire - foyer 20 m');family(cases,'cable',20,f11,'Câble principal - foyer 20 m')
 annex=[]
 for fn in curves:
  for el,lab in [('hanger','Suspente secondaire'),('cable','Câble principal clos')]:p=PNG/f'B_{fn}_{el}.png';envelope(cases,fn,el,p,f'{fn} - {lab}');annex.append((p,f'{fn} - {lab} : cas et enveloppe maximale.'))
 temps=pd.DataFrame([[t,round(max(c['hanger'][np.argmin(abs(tm-t))] for c in cases),1),round(max(c['cable'][np.argmin(abs(tm-t))] for c in cases),1)] for t in TIMES],columns=['Temps (min)','Suspente (°C)','Câble principal (°C)'])
 rows=[];maxlines=[]
 for fn in curves:
  sel=[c for c in cases if c['fire']==fn]
  for el,label,E,N,F in [('hanger','Suspente secondaire',E_HANGER,N_HANGER,FTRD_HANGER),('cable','Câble principal clos',E_CABLE,N_CABLE,FTRD_CABLE)]:
   env=np.max(np.vstack([c[el] for c in sel]),axis=0);ratio=N/(ky(env)*F);ok=np.where(ratio<=1)[0];tmax=tm[ok[-1]] if len(ok) else 0;maxlines.append(f'{label} - {fn} : {tmax:.1f} min')
   for t in TIMES:
    i=np.argmin(abs(tm-t));T=env[i];k_y=float(ky(T));k_e=float(ke(T));rd=k_y*F;eta=N/rd if rd>0 else np.inf;rows.append([fn,t,label,round(T,1),round(k_y,3),round(k_e*E,1),round(rd,1),round(eta,3),'Justifié' if eta<=1 else 'Non justifié'])
 struct=pd.DataFrame(rows,columns=['Feu','t (min)','Organe','θ (°C)','ky,θ','Eθ (GPa)','Ft,Rd,θ (kN)','ηfi','Statut'])
 ctx={'assets':[(ASSETS/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.',16),(ASSETS/'ZZ extrait plan suspension.png','Figure 2 - Système de suspension.',16),(ASSETS/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale.',16),(ASSETS/'ZZ coupe transv.png','Figure 4 - Coupe transversale.',16)],'cerema':ASSETS/'extrait_cerema_choix_courbes.png','fire':firep,'intrados':ASSETS/'ZZ_approxim intrados demi-coupe.png','f10':f10,'f11':f11,'annex':annex,'temps':temps,'struct':struct,'maxtext':'Temps maximal évalué par organe et par feu, sur le pas de calcul de 5 s : '+' ; '.join(maxlines)+'.','geomtab':pd.DataFrame([[p['code'],p['deck'],p['hanger'],p['cable']] for p in POS],columns=['Coupe','Intrados','Suspente','Câble']),'params':pd.DataFrame([['E câble principal','160 GPa'],['NQP câble principal','3 300 kN'],['Ft,Rd câble principal','11 897 kN'],['E suspente secondaire','205 GPa'],['NQP suspente secondaire','115 kN'],['Ft,Rd suspente secondaire','541 kN']],columns=['Paramètre','Valeur'])}
 print(build(ctx,REPORTS/REPORT))
if __name__=='__main__':main()
