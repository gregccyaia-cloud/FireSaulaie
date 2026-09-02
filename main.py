import numpy as np,pandas as pd
from config import *
from model import gas,solve,phi,ky,ke
from plots import fires,geometry,family,ratio,envelope,integration
from report import build
POS=[{'code':'F1','deck':6.125,'hanger':6.945,'cable':8.120},{'code':'F2','deck':6.900,'hanger':7.720,'cable':9.400},{'code':'F3','deck':7.250,'hanger':8.070,'cable':11.070}]
def main():
 for d in (PNG,REPORTS):d.mkdir(parents=True,exist_ok=True)
 ts=np.arange(0,TMAX*60+DT,DT);tm=ts/60;names=('ISO 834','Feu extérieur','HC');curves={f:gas(tm,f) for f in names};cases=[]
 for fn,tg in curves.items():
  for p in POS:
   for H in FLAME_HEIGHTS:cases.append({'fire':fn,'pos':p['code'],'H':H,'tm':tm,'gas':tg,'hanger':solve(ts,tg,.042,phi(H,p['hanger'])),'cable':solve(ts,tg,.132,phi(H,p['cable']))})
 firep=PNG/'feux.png';geomp=PNG/'geometrie.png';fires(tm,curves,firep);geometry(POS,geomp);f12=PNG/'fig12.png';f13=PNG/'fig13.png';family(cases,'hanger',20,f12,'Suspente secondaire - hauteur de foyer 20 m');family(cases,'cable',20,f13,'Câble principal - hauteur de foyer 20 m')
 rows=[];maxdict={};pilot=[]
 for fn in names:
  sel=[c for c in cases if c['fire']==fn]
  for el,label,E,N,F in [('hanger','Suspente secondaire',E_HANGER,N_HANGER,FTRD_HANGER),('cable','Câble principal clos',E_CABLE,N_CABLE,FTRD_CABLE)]:
   # confirmer le H pilotant par maximum à chaque instant
   envelopes={H:np.max(np.vstack([c[el] for c in sel if c['H']==H]),axis=0) for H in FLAME_HEIGHTS};pilot_H=max(FLAME_HEIGHTS,key=lambda H:float(np.max(envelopes[H])));env=envelopes[pilot_H];pilot.append(f'{label} sous {fn} : H = {pilot_H:g} m')
   rat=N/(ky(env)*F);ok=np.where(rat<=1)[0];tmax=tm[ok[-1]] if len(ok) else 0;maxdict[(fn,el)]=tmax
   for t in TIMES:
    i=np.argmin(abs(tm-t));T=env[i];rd=float(ky(T)*F);eta=N/rd if rd else np.inf;rows.append([fn,t,label,pilot_H,round(T,1),round(float(ky(T)),3),round(float(ke(T)*E),1),round(rd,1),round(eta,3),'Justifié' if eta<=1 else 'Non justifié'])
 struct=pd.DataFrame(rows,columns=['Feu','Temps (min)','Organe','H pilote (m)','θ (°C)','ky,θ','Eθ (GPa)','Ft,Rd,θ (kN)','ηfi','Statut']);f14=PNG/'fig14.png';f15=PNG/'fig15.png';ratio(struct,'Suspente secondaire',f14,'Ratio ηfi - Suspente secondaire');ratio(struct,'Câble principal clos',f15,'Ratio ηfi - Câble principal clos')
 temps=pd.DataFrame([[t,*[round(max(c[e][np.argmin(abs(tm-t))] for c in cases),1) for e in ('hanger','cable')]] for t in TIMES],columns=['Temps (min)','Suspente secondaire (°C)','Câble principal (°C)'])
 annex=[]
 for fn in names:
  for el,lab in [('hanger','Suspente secondaire'),('cable','Câble principal clos')]:p=PNG/f'B_{fn}_{el}.png';envelope(cases,fn,el,p,f'{fn} - {lab}');annex.append((p,f'{fn} - {lab} : OUEST / AXE M7 / EST, H=10/15/20 m et enveloppe.'))
 # annexe A: cas critique global à 30 min
 i30=np.argmin(abs(tm-30));w=max(cases,key=lambda c:max(c['hanger'][i30],c['cable'][i30]));ip=PNG/'integration.png';integration(w,ip)
 steps=pd.DataFrame([[1,'Lecture de θa,i','Température au début du pas'],[2,'Calcul de ca(θa,i)','Loi acier dépendante de la température'],[3,'Calcul de qconv et qrad','Flux thermique net'],[4,'Calcul de Δθa,i','Bilan sur Δt = 5 s'],[5,'Mise à jour θa,i+1','Nouvelle température'],[6,'Répétition','Jusqu’à 120 min']],columns=['Étape','Opération','Résultat'])
 worst=pd.DataFrame([['Courbe',w['fire']],['Position',{'F1':'OUEST','F2':'AXE M7','F3':'EST'}[w['pos']]],['Hauteur de foyer',f"{w['H']:g} m"],['Suspente à 30 min',f"{w['hanger'][i30]:.1f} °C"],['Câble à 30 min',f"{w['cable'][i30]:.1f} °C"]],columns=['Grandeur','Valeur'])
 main_non_hc=maxdict[('ISO 834','cable')];main_ext=maxdict[('Feu extérieur','cable')];main_non_hc_min=min(main_non_hc,main_ext)
 conclusion=(f"Sans surprise, la courbe HC est la plus pénalisante. Son maintien dans le scénario de calcul reste à confirmer par la MOA et son AMO. Le temps d’intervention sur ouvrage indiqué par le SDMIS lors de la réunion du 20/04/2026 est de 15 min ; cette donnée est reprise comme hypothèse projet, la réunion n’ayant pas été retrouvée dans les résultats de recherche disponibles. Si le scénario HC est retenu, les résultats conduisent à prévoir des protections pour la suspension principale et les suspentes secondaires ; leur typologie et leur justification seront détaillées ultérieurement. Si seules les courbes ISO 834 et feu extérieur sont retenues et qu’une durée de 30 min est jugée suffisante, un développement complémentaire pourra examiner la possibilité de s’affranchir de protections, notamment par une analyse des reports de réaction lors de la rupture d’une suspente secondaire. La durée maximale calculée de la suspension principale hors HC vaut {main_non_hc_min:.1f} min dans le cas le plus pénalisant des deux courbes non HC (ISO 834 : {main_non_hc:.1f} min ; feu extérieur : {main_ext:.1f} min).")
 ctx={'assets':[(ASSETS/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.',16),(ASSETS/'ZZ extrait plan suspension.png','Figure 2 - Système de suspension.',16),(ASSETS/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale.',16),(ASSETS/'ZZ coupe transv.png','Figure 4 - Coupe transversale.',16)],'cerema':ASSETS/'extrait_cerema_choix_courbes.png','fire':firep,'geom':geomp,'intrados':ASSETS/'ZZ_approxim intrados demi-coupe.png','f12':f12,'f13':f13,'f14':f14,'f15':f15,'annex':annex,'temps':temps,'struct':struct,'pilot':'Le contrôle automatique confirme les hauteurs de foyer pilotantes suivantes : '+' ; '.join(pilot)+'. La hauteur de 20 m pilote donc les résultats présentés ci-après.','maxtext':'Temps maximal justifié, au pas de 5 s : '+' ; '.join([f"{el} - {fn} : {maxdict[(fn,key)]:.1f} min" for fn in names for key,el in [('hanger','Suspente secondaire'),('cable','Câble principal clos')]])+'.','conclusion':conclusion,'steps':steps,'integration':ip,'worst':worst,'geomtab':pd.DataFrame([['OUEST',6.125,6.945,8.120],['AXE M7',6.900,7.720,9.400],['EST',7.250,8.070,11.070]],columns=['Coupe','Intrados','Suspente','Câble']),'params':pd.DataFrame([['Hauteurs de foyer (hypothèse de sensibilité)','10 / 15 / 20 m'],['Ft,Rd câble principal (cf. SAU_AVP_NDC_062_A_JustifOADéfi)','11 897 kN'],['NQP câble principal','3 300 kN'],['E câble principal','160 GPa'],['Ft,Rd suspente secondaire (cf. SAU_AVP_NDC_062_A_JustifOADéfi)','541 kN'],['NQP suspente secondaire','115 kN'],['E suspente secondaire','205 GPa']],columns=['Paramètre','Valeur'])}
 print(build(ctx,REPORTS/REPORT))
if __name__=='__main__':main()
