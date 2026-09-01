import numpy as np,pandas as pd
from data.config import *
from data.project import *
from models.fire import scenarios
from models.geometry import geometry,key
from models.thermal import amv_circle,solve
from plotting.plots import fire_plot,equation_plot,principles_plot,case_plot,family_plot
from reporting.report import build_report

def run_case(s,p,hf,time_s):
 tm=time_s/60.;tg=s.temperature(tm);g=geometry(p,hf);data={'time_min':tm,'T_gas':tg};meta={}
 for name,amv,h in [('deck',DECK_AMV,g['h_deck_m']),('hanger',amv_circle(HANGER_D),g['h_hanger_m']),('cable',amv_circle(CABLE_D),g['h_cable_m'])]:
  k=key(name,h,hf);fr,fc=EXPOSURE[k];T,qc,qr,cp,dT=solve(time_s,tg,amv,fr,fc)
  for lab,val in [('T',T),('qc',qc),('qr',qr),('cp',cp),('dT',dT)]:data[f'{lab}_{name}']=val
  meta[name]={'amv':amv,'fr':fr,'fc':fc}
 return pd.DataFrame(data),g,meta

def main():
 for d in (PNG_DIR,CSV_DIR,REPORT_DIR,LOG_DIR):d.mkdir(parents=True,exist_ok=True)
 time_s=np.arange(0,DURATION_MIN*60+DT_S,DT_S);sc=scenarios();fire_png=PNG_DIR/'01_courbes_feu.png';eq_png=PNG_DIR/'00_formules_feu.png';pr_png=PNG_DIR/'02_formules_thermiques.png';fire_plot(time_s/60,sc,fire_png);equation_plot(eq_png);principles_plot(pr_png)
 allcases=[];rows=[];appendix=[]
 for s in sc:
  for p in POSITIONS:
   for hf in FLAME_HEIGHTS:
    df,g,m=run_case(s,p,hf,time_s);stem=f'{s.code}_{p.code}_H{int(hf)}';df.to_csv(CSV_DIR/f'{stem}.csv',sep=';',decimal=',',index=False);png=PNG_DIR/f'{stem}.png';case_plot(df,f'{s.label} - {p.label} - H = {hf:.0f} m',png)
    allcases.append((stem,s,p,hf,df,g,m,png));appendix.append((png,f'{stem} : évolution des températures du gaz, de l’intrados, de la suspente et du câble principal.'));rows.append({'Cas':stem,'Tmax intrados (°C)':round(df.T_deck.max(),1),'Tmax suspente (°C)':round(df.T_hanger.max(),1),'Tmax câble (°C)':round(df.T_cable.max(),1)})
 summary=pd.DataFrame(rows);summary.to_csv(CSV_DIR/'SYNTHESE.csv',sep=';',decimal=',',index=False)
 hanger_png=PNG_DIR/'03_suspentes_H15.png';cable_png=PNG_DIR/'04_cables_H15.png';family_plot(allcases,'hanger',15.,hanger_png,'Échauffement - Suspente secondaire - H = 15 m');family_plot(allcases,'cable',15.,cable_png,'Échauffement - Câble principal clos - H = 15 m')
 idx=int(round(30*60/DT_S));c=[]
 for stem,s,p,hf,df,g,m,png in allcases:
  for e in ('deck','hanger','cable'):c.append((float(df.loc[idx,f'T_{e}']),stem,s,p,hf,df,m[e],png,e))
 _,stem,s,p,hf,df,me,png,e=max(c,key=lambda x:x[0]);i=idx;labels={'deck':'intrados','hanger':'suspente','cable':'câble principal'};w={'case':stem,'fire':s.label,'position':p.label,'hf':hf,'element':labels[e],'amv':me['amv'],'fr':me['fr'],'fc':me['fc'],'dt':DT_S,'Tg_start':float(df.loc[i-1,'T_gas']),'T_start':float(df.loc[i-1,f'T_{e}']),'cp':float(df.loc[i,f'cp_{e}']),'qc':float(df.loc[i,f'qc_{e}']),'qr':float(df.loc[i,f'qr_{e}']),'dT':float(df.loc[i,f'dT_{e}']),'T_end':float(df.loc[i,f'T_{e}']),'png':png}
 wr=[["Courbe de feu",w['fire']],["Position du camion",w['position']],["Hauteur d’enveloppe",f"{w['hf']:.2f} m"],["Élément",w['element']],["A_m/V",f"{w['amv']:.3f} m⁻¹"],["f_rad",f"{w['fr']:.3f}"],["f_conv",f"{w['fc']:.3f}"],["Pas",f"{w['dt']:.1f} s"],["T_g à 29 min 55 s",f"{w['Tg_start']:.3f} °C"],["T_acier à 29 min 55 s",f"{w['T_start']:.3f} °C"],["c_a",f"{w['cp']:.3f} J/(kg·K)"],["q_conv",f"{w['qc']:.3f} W/m²"],["q_rad",f"{w['qr']:.3f} W/m²"],["q_net",f"{w['qc']+w['qr']:.3f} W/m²"],["ΔT du dernier pas",f"{w['dT']:.6f} °C"],["T_acier à 30 min",f"{w['T_end']:.3f} °C"]]
 we=f"ΔT = {w['amv']:.3f} × ({w['qc']:.3f} + {w['qr']:.3f}) × {w['dt']:.1f} / (7 850 × {w['cp']:.3f}) = {w['dT']:.6f} °C"
 ctx={'coupe':ASSET_DIR/'coupe_transversale.png','demicoupe':ASSET_DIR/'demi_coupe_intrados.png','eq_png':eq_png,'fire_png':fire_png,'principles_png':pr_png,'hanger_png':hanger_png,'cable_png':cable_png,'all_figures':appendix,'summary':summary,'worst':w,'worst_rows':wr,'worst_equation':we,
 'project':[['M7','2 × 3 voies ; largeur simplifiée 13 + 2 + 12 m'],['Tablier','largeur totale 7,40 m'],['Intrados minimal','6,125 / 6,900 / 7,250 m'],['Câble principal','câble clos Ø132 mm ; acier nu'],['Suspentes','ronds Ø42 mm ; entraxe 6,25 m'],['Position basse des suspentes','0,82 m au-dessus du point bas de l’intrados']],
 'hypotheses':[['Courbes de feu','ISO 834 et feu extérieur CEREMA','Calculs séparés, puis enveloppe'],['Durée','120 min ; lectures à 15, 30, 60, 90 et 120 min','Retenu'],['Camion','16 × 2,5 × 4 m','Hypothèse V1.4'],['Positions','F1 ouest ; F2 axe M7 ; F3 est','Repères introduits'],['Enveloppes de flamme','10, 12 et 15 m','Analyse de sensibilité'],['Câble principal','Ø132 mm, câble clos acier nu','Donnée projet'],['PEHD','Variante non activée','Étape ultérieure'],['Modèle thermique','Température uniforme par élément','V1.4'],['Exposition spatiale','Coefficients directs ou masqués','Provisoire']],
 'thermal':[['ρ acier','7 850 kg/m³'],['α_c','25 W/(m²·K)'],['ε_m / ε_f','0,70 / 1,00'],['σ','5,670374419 × 10⁻⁸ W/(m²·K⁴)'],['A_m/V suspente','95,238 m⁻¹'],['A_m/V câble','30,303 m⁻¹'],['A_m/V intrados','100 m⁻¹, provisoire'],['Pas temporel','5 s']],
 'conclusions':['Les mentions demandées ont été supprimées et les légendes harmonisées.','Les positions F1, F2 et F3 sont introduites avant leur première utilisation.','Les formules sont rendues par Matplotlib en notation mathématique afin de positionner correctement indices et exposants.','Les deux graphiques de familles comportent six courbes pour H = 15 m : deux feux et trois positions.','L’annexe B rassemble les courbes des 18 cas étudiés.','Les coefficients d’exposition et le facteur de massiveté de l’intrados restent à justifier avant dimensionnement.']}
 out=REPORT_DIR/REPORT_FILENAME
 if GENERATE_REPORT:build_report(ctx,out);print(f'[OK] Rapport généré : {out.resolve()}')
 print(f"[OK] Worst case 30 min : {w['case']} / {w['element']} / {w['T_end']:.2f} °C")
if __name__=='__main__':main()
