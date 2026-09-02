import numpy as np,pandas as pd
from config import *
from fire import CURVES
from model import solve,phi
from plots import fire,geom,family,envelope,integration
from report import build
POS=[{'code':'F1','deck':6.125,'hanger':6.945,'cable':8.120},{'code':'F2','deck':6.900,'hanger':7.720,'cable':9.400},{'code':'F3','deck':7.250,'hanger':8.070,'cable':11.070}]
def main():
 for d in (PNG,CSV,REPORTS):d.mkdir(parents=True,exist_ok=True)
 ts=np.arange(0,TMAX*60+DT,DT);tm=ts/60;curves={k:f(tm) for k,f in CURVES.items()};cases=[]
 firep=PNG/'feu.png';geomp=PNG/'geom.png';fire(tm,curves,firep);geom(POS,geomp)
 for fname,tg in curves.items():
  for p in POS:
   for L in LENGTHS:
    Th,qc,qr,cp,di=solve(ts,tg,.042,phi(L,p['hanger']));Tc,*_=solve(ts,tg,.132,phi(L,p['cable']));df=pd.DataFrame({'time_min':tm,'T_hanger':Th,'T_cable':Tc});df.to_csv(CSV/f'{fname}_{p["code"]}_{int(L)}.csv',sep=';',decimal=',',index=False);cases.append({'fire':fname,'pos':p['code'],'L':L,'tm':tm,'gas':tg,'hanger':Th,'cable':Tc,'df':df,'qc':qc,'qr':qr,'cp':cp,'di':di})
 f10=PNG/'fig10.png';f11=PNG/'fig11.png';family(cases,'hanger',20.,f10,'Échauffement - Suspente secondaire - foyer 20 m');family(cases,'cable',20.,f11,'Échauffement - Câble principal clos - foyer 20 m')
 annex=[]
 for fn in CURVES:
  for el,lab in [('hanger','Suspente secondaire'),('cable','Câble principal clos')]:p=PNG/f'B_{fn}_{el}.png';envelope(cases,fn,el,p,f'{fn} - {lab} - enveloppe');annex.append((p,f'Figure B - {fn} - {lab} : cas et enveloppe maximale.'))
 retained=[]
 for t in TIMES:
  i=np.argmin(abs(tm-t));retained.append([t,round(max(c['hanger'][i] for c in cases),1),round(max(c['cable'][i] for c in cases),1)])
 retained=pd.DataFrame(retained,columns=['Temps (min)','Suspente secondaire (°C)','Câble principal clos (°C)'])
 i=np.argmin(abs(tm-30));w=max(cases,key=lambda c:max(c['hanger'][i],c['cable'][i]));ip=PNG/'integration.png';integration(w,ip)
 assets=[(ASSETS/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.',16),(ASSETS/'ZZ extrait plan suspension.png','Figure 2 - Élévation et plan du système de suspension.',16),(ASSETS/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale générale.',16),(ASSETS/'ZZ coupe transv.png','Figure 4 - Coupe transversale type.',16),(ASSETS/'ZZ_demie coupe tablier et approx intrados.png','Figure 5 - Demi-coupe et approximation de l’intrados par 2 segments de droite.',16),(ASSETS/'ZZ_approxim intrados demi-coupe.png','Figure 5 bis - Schéma de principe de l’approximation de l’intrados par deux segments de droite, avec les points géométriques de calage.',14)]
 params=pd.DataFrame([['Poids lourd','16,0 × 2,50 × 4,00 m'],['Longueurs de foyer','10 / 15 / 20 m'],['Pas Δt','5 s'],['αc','25 W/(m²·K)'],['εm / εf','0,70 / 1,00'],['ca(θa)','Loi NF EN 1993-1-2 mise à jour à chaque pas']],columns=['Paramètre','Valeur'])
 geometry=pd.DataFrame([[p['code'],p['deck'],p['hanger'],p['cable']] for p in POS],columns=['Coupe','Intrados (m)','Suspente (m)','Câble (m)'])
 steps=pd.DataFrame([[1,'Lecture de θa,i'],[2,'Calcul de ca(θa,i)'],[3,'Calcul des flux'],[4,'Calcul de Δθa,i'],[5,'Mise à jour θa,i+1'],[6,'Répétition jusqu’à 120 min']],columns=['Étape','Opération'])
 worst=pd.DataFrame([['Cas',f"{w['fire']} - {w['pos']} - {w['L']:g} m"],['Température suspente à 30 min',f"{w['hanger'][i]:.2f} °C"],['Température câble à 30 min',f"{w['cable'][i]:.2f} °C"]],columns=['Grandeur','Valeur'])
 ctx={'assets':assets,'cerema':ASSETS/'extrait_cerema_choix_courbes.png','fire':firep,'geom':geomp,'f10':f10,'f11':f11,'retained':retained,'params':params,'geometry':geometry,'steps':steps,'worst':worst,'integration':ip,'annex':annex,'choice':'En appui du guide Cerema, les courbes CN - ISO 834 et feu extérieur sont étudiées séparément puis comparées.','moa':'Il appartient au maître d’ouvrage ou à son AMO de confirmer à la MOE si la courbe HC doit également être étudiée.','cp':'La chaleur spécifique ca dépend de θa et est recalculée à chaque pas selon la NF EN 1993-1-2.'}
 print(build(ctx,REPORTS/REPORT))
if __name__=='__main__':main()
