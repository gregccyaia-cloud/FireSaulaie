import numpy as np,pandas as pd
from data.config import *
from data.project import *
from models.fire import scenarios
from models.thermal import solve,phi_rectangle,amv
from plotting.plots import fire_curves,geometry,family,envelope,integration
from reporting.report import build

def main():
 for d in (CSV,PNG,REPORTS,LOGS):d.mkdir(parents=True,exist_ok=True)
 ts=np.arange(0,DURATION_MIN*60+DT_S,DT_S);tm=ts/60.;sc=scenarios();cases=[];rows=[]
 fire_png=PNG/'courbes_feu.png';geo_png=PNG/'geometrie.png';fire_curves(tm,sc,fire_png);geometry(POSITIONS,geo_png)
 for s in sc:
  tg=s.temperature(tm)
  for p in POSITIONS:
   for L in FOYER_LENGTHS:
    ph=phi_rectangle(L,p.h_hanger);pc=phi_rectangle(L,p.h_cable)
    Th,qch,qrh,cph,dth=solve(ts,tg,HANGER_D,ph);Tc,qcc,qrc,cpc,dtc=solve(ts,tg,CABLE_D,pc)
    df=pd.DataFrame({'time_min':tm,'T_gas':tg,'T_hanger':Th,'T_cable':Tc,'phi_hanger':ph,'phi_cable':pc,'qconv_hanger':qch,'qrad_hanger':qrh,'cp_hanger':cph,'dT_hanger':dth})
    stem=f'{s.code}_{p.code}_L{int(L)}';df.to_csv(CSV/f'{stem}.csv',sep=';',decimal=',',index=False);cases.append({'fire':s.code,'pos':p.code,'L':L,'df':df,'stem':stem})
    for name,col in [('Suspente secondaire','T_hanger'),('Câble principal clos','T_cable')]:rows.append([s.label,p.code,int(L),name,*[round(float(np.interp(t,tm,df[col])),1) for t in READ_TIMES]])
 summary=pd.DataFrame(rows,columns=['Feu','Position','L (m)','Élément',*['T '+str(t)+' min (°C)' for t in READ_TIMES]])
 f10=PNG/'fig10_suspente.png';f11=PNG/'fig11_cable.png';family(cases,'hanger',15.,f10,'Échauffement - Suspente secondaire - foyer 15 m');family(cases,'cable',15.,f11,'Échauffement - Câble principal clos - foyer 15 m')
 annex=[]
 for fire,label in [('ISO834','ISO 834'),('EXTERIEUR','Feu extérieur')]:
  for el,lab in [('hanger','Suspente secondaire'),('cable','Câble principal clos')]:
   pth=PNG/f'annexe_{fire}_{el}.png';envelope(cases,fire,el,pth,f'{label} - {lab} - enveloppe de tous les cas');annex.append((pth,f'Figure B - {label} - {lab} : cas individuels et enveloppe maximale.'))
 idx=int(30*60/DT_S);worst=max(cases,key=lambda c:max(c['df'].loc[idx,'T_hanger'],c['df'].loc[idx,'T_cable']));df=worst['df'];el='hanger' if df.loc[idx,'T_hanger']>=df.loc[idx,'T_cable'] else 'cable';integ=PNG/'integration.png';integration(df,integ)
 wrows=[['Cas',worst['stem']],['Élément','Suspente secondaire' if el=='hanger' else 'Câble principal clos'],['Φ',f"{float(df.loc[idx,'phi_'+el]):.3f}"],['A_m/V',f"{amv(HANGER_D if el=='hanger' else CABLE_D):.3f} m⁻¹"],['θg à 29 min 55 s',f"{df.loc[idx-1,'T_gas']:.2f} °C"],['θa à 29 min 55 s',f"{df.loc[idx-1,'T_'+el]:.2f} °C"],['qconv',f"{df.loc[idx,'qconv_hanger']:.1f} W/m²" if el=='hanger' else 'voir CSV'],['qrad',f"{df.loc[idx,'qrad_hanger']:.1f} W/m²" if el=='hanger' else 'voir CSV'],['ca',f"{df.loc[idx,'cp_hanger']:.1f} J/(kg·K)" if el=='hanger' else 'voir CSV'],['θa à 30 min',f"{df.loc[idx,'T_'+el]:.2f} °C"]]
 assets=[(ASSETS/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.',16),(ASSETS/'ZZ extrait plan suspension.png','Figure 2 - Élévation et plan du système de suspension.',16),(ASSETS/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale générale.',16),(ASSETS/'ZZ coupe transv.png','Figure 4 - Coupe transversale type du tablier.',16)]
 ctx={'project_assets':assets,'cerema':ASSETS/'extrait_cerema_choix_courbes.png','fire':fire_png,'geometry':geo_png,'f10':f10,'f11':f11,'integration':integ,'annex':annex,'summary':summary,
 'choice':"En appui du guide Cerema, rubrique « Choix des courbes », les courbes CN - ISO 834 et feu extérieur sont utilisées. Elles sont calculées séparément puis comparées.",
 'moa':"Il appartient néanmoins au maître d’ouvrage ou à son AMO de préciser à la MOE si la courbe HC doit être utilisée, le maître d’ouvrage devant définir le scénario de feu contre lequel il souhaite protéger l’ouvrage.",
 'tanker':"Les longueurs de foyer étudiées jusqu’à 20 m et les courbes non HC ne couvrent pas un feu de camion-citerne ou un scénario hydrocarboné sévère.",
 'geometry_rows':[[p.code,f'{p.h_deck:.3f}',f'{p.h_hanger:.3f}',f'{p.h_cable:.3f}'] for p in POSITIONS],
 'params':[['Poids lourd (hypothèse projet)','16,0 × 2,50 × 4,00 m'],['Longueur de foyer (analyse de sensibilité)','10 / 15 / 20 m'],['Durée du calcul','120 min'],['Pas de temps','5 s'],['Facteur de forme Φ (NF EN 1991-1-2, § 3.1)','calcul géométrique de sensibilité, borné à 1,0'],['Coefficient convectif αc (NF EN 1991-1-2, § 3.1)','25 W/(m²·K)'],['Émissivité acier εm','0,70'],['Émissivité flamme εf','1,00'],['Facteur d’ombre ksh (NF EN 1993-1-2)','1,00']],
 'cp_text':"La chaleur spécifique ca(θa) est recalculée à chaque pas suivant les domaines de température de la NF EN 1993-1-2 : 20-600 °C, 600-735 °C, 735-900 °C et 900-1 200 °C.",
 'method':"Pour chaque courbe, position et longueur de foyer, le calcul évalue la température des gaz, le facteur de forme, les flux convectif et radiatif, puis l’incrément de température de l’acier. L’intégration est répétée par pas de 5 s jusqu’à 120 min.",
 'structural':"Les historiques θ(t) permettront ensuite de déterminer les propriétés mécaniques réduites et de comparer les résistances aux efforts axiaux à préciser dans les suspentes principales et secondaires. L’ELS quasi-permanent peut servir de donnée initiale, sous réserve de définir la combinaison accidentelle de calcul au feu.",
 'limits':"L’approche du présent rapport est une analyse thermique simplifiée. Le facteur de forme est un affinement géométrique de sensibilité et devra être validé avec la géométrie rayonnante et les effets de masque. Le scénario ne couvre pas un feu de citerne.",
 'steps':[['0','Initialisation','θa=20 °C'],['1','Température des gaz','ISO 834 ou feu extérieur'],['2','Facteur de forme Φ','fonction de L et de la hauteur du récepteur'],['3','Chaleur spécifique ca','mise à jour selon θa'],['4','Flux qconv et qrad','W/m²'],['5','Incrément Δθa','pas de 5 s'],['6','Boucle','jusqu’à 120 min'],['7','Extraction','15, 30, 60, 90, 120 min']], 'worst_rows':wrows,'worst_eq':'La température à 30 min résulte de la somme des incréments successifs depuis t=0 ; les valeurs détaillées sont conservées dans le CSV du cas.'}
 out=build(ctx,REPORTS/REPORT_NAME);print('[OK]',out);print('[OK] Modification système',out.stat().st_mtime)
if __name__=='__main__':main()
