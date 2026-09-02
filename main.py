import numpy as np,pandas as pd
from config import *
from model import gas,solve,phi,ky,ke,TEMP,KY,KE
from plots import fires,family,ratios,envelope,integration
from report import build
POS=[{'code':'F1','deck':6.125,'hanger':6.945,'cable':8.120},{'code':'F2','deck':6.900,'hanger':7.720,'cable':9.400},{'code':'F3','deck':7.250,'hanger':8.070,'cable':11.070}];PL={'F1':'OUEST','F2':'AXE M7','F3':'EST'}
def main():
 for d in (PNG,REPORTS):d.mkdir(parents=True,exist_ok=True)
 ts=np.arange(0,TMAX*60+DT,DT);tm=ts/60;names=('ISO 834','Feu extérieur','HC');curves={f:gas(tm,f) for f in names};cases=[]
 for fn,tg in curves.items():
  for p in POS:
   for H in HEIGHTS:cases.append({'fire':fn,'pos':p['code'],'H':H,'t':tm,'gas':tg,'hanger':solve(ts,tg,.042,phi(H,p['hanger'])),'cable':solve(ts,tg,.132,phi(H,p['cable']))})
 firep=PNG/'feux.png';fires(tm,curves,firep);f12=PNG/'fig12.png';f13=PNG/'fig13.png';family(cases,'hanger',20,f12,'Suspente secondaire - hauteur de foyer 20 m');family(cases,'cable',20,f13,'Câble principal - hauteur de foyer 20 m')
 rows=[];mt={}
 for fn in names:
  for pos in POS:
   c=next(x for x in cases if x['fire']==fn and x['pos']==pos['code'] and x['H']==20)
   for el,label,E,N,F in [('hanger','Suspente secondaire',E_HANGER,N_HANGER,FTRD_HANGER),('cable','Câble principal clos',E_CABLE,N_CABLE,FTRD_CABLE)]:
    r=N/(ky(c[el])*F);ok=np.where(r<=1)[0];mt[(fn,pos['code'],el)]=tm[ok[-1]] if len(ok) else 0
    for t in TIMES:
     i=np.argmin(abs(tm-t));T=c[el][i];k=float(ky(T));ee=float(ke(T));rd=k*F;eta=N/rd if rd else np.inf;rows.append([fn,PL[pos['code']],t,label,round(T,1),round(k,3),round(ee,3),round(ee*E,1),round(rd,1),round(eta,3),'Justifié' if eta<=1 else 'Non justifié'])
 struct=pd.DataFrame(rows,columns=['Feu','Position','Temps','Organe','θ','ky,θ','kE,θ','Eθ','Ft,Rd,θ','ηfi','Statut']);f14=PNG/'fig14.png';f15=PNG/'fig15.png';ratios(struct,'Suspente secondaire',f14,'Ratio ηfi - Suspente secondaire');ratios(struct,'Câble principal clos',f15,'Ratio ηfi - Câble principal clos')
 temps=pd.DataFrame([[t,round(max(c['hanger'][np.argmin(abs(tm-t))] for c in cases),1),round(max(c['cable'][np.argmin(abs(tm-t))] for c in cases),1)] for t in TIMES],columns=['Temps','Suspente','Câble principal'])
 annex=[]
 for fn in names:
  for el,lab in [('hanger','Suspente secondaire'),('cable','Câble principal clos')]:p=PNG/f'B_{fn}_{el}.png';envelope(cases,fn,el,p,f'{fn} - {lab}');annex.append((p,f'{fn} - {lab} : OUEST / AXE M7 / EST, H=10/15/20 m et enveloppe.'))
 i=np.argmin(abs(tm-30));w=max(cases,key=lambda c:max(c['hanger'][i],c['cable'][i]));ip=PNG/'integration.png';integration(w,ip)
 def m(el,fn):return min(mt[(fn,p,el)] for p in ('F1','F2','F3'))
 cb=[(fn,f'{m("cable",fn):.1f} min',fn=='HC') for fn in names];hb=[(fn,f'{m("hanger",fn):.1f} min',fn=='HC') for fn in names];nonhc=min(m('cable','ISO 834'),m('cable','Feu extérieur'))
 conclusion=f'Sans surprise, le feu HC est le plus pénalisant. Son maintien reste à confirmer par la MOA et son AMO. Le temps d’intervention sur ouvrage indiqué par le SDMIS en réunion du 20/04/2026 est de 15 min. Si le scénario HC est retenu, des protections de la suspension principale et des suspentes secondaires sont à prévoir. Si seules ISO 834 et feu extérieur sont retenues et qu’une durée de 30 min est jugée suffisante, des calculs complémentaires pourraient examiner les reports de réaction lors de la rupture d’une suspente secondaire. La durée maximale calculée de la suspension principale hors HC vaut {nonhc:.1f} min. A fortiori, un foyer de 30 m serait plus pénalisant que l’enveloppe de 20 m et nécessiterait une nouvelle série de calculs.'
 ctx={'assets':[(ASSETS/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.',16),(ASSETS/'ZZ extrait plan suspension.png','Figure 2 - Système de suspension.',16),(ASSETS/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale.',16),(ASSETS/'ZZ coupe transv.png','Figure 4 - Coupe transversale.',16)],'cerema':ASSETS/'extrait_cerema_choix_courbes.png','fire':firep,'planm7':ASSETS/'ZZ_vue en plan cotée zone M7.png','coupeM7':ASSETS/'ZZ_coupe longit partielle zone M7.png','intrados':ASSETS/'ZZ_approxim intrados demi-coupe.png','f12':f12,'f13':f13,'f14':f14,'f15':f15,'annex':annex,'temps':temps,'struct':struct,'ky':pd.DataFrame({'θ':TEMP,'ky,θ':KY,'kE,θ':KE}),'cb':cb,'hb':hb,'conclusion':conclusion,'steps':pd.DataFrame([[1,'Lecture θa,i'],[2,'Calcul ca(θa,i)'],[3,'Calcul des flux'],[4,'Calcul Δθa,i'],[5,'Mise à jour θa,i+1'],[6,'Répétition jusqu’à 120 min']],columns=['Étape','Opération']),'integration':ip,'worst':pd.DataFrame([['Courbe',w['fire']],['Position',PL[w['pos']]],['Hauteur',w['H']],['Suspente à 30 min',round(w['hanger'][i],1)],['Câble à 30 min',round(w['cable'][i],1)]],columns=['Grandeur','Valeur']),'geomtab':pd.DataFrame([['OUEST',6.125,6.945,8.120],['AXE M7',6.900,7.720,9.400],['EST',7.250,8.070,11.070]],columns=['Coupe','Intrados','Suspente','Câble']),'params':pd.DataFrame([['Hauteurs de foyer','10 / 15 / 20 m'],['Ft,Rd câble principal','11 897 kN'],['NQP câble principal','3 300 kN'],['E câble principal','160 GPa'],['Ft,Rd suspente secondaire','541 kN'],['NQP suspente secondaire','115 kN'],['E suspente secondaire','205 GPa']],columns=['Paramètre','Valeur'])}
 print(build(ctx,REPORTS/REPORT))
if __name__=='__main__':main()
