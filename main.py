import numpy as np,pandas as pd
from data.config import *
from data.project import *
from models.fire import scenarios
from models.geometry import geometry,key
from models.thermal import amv_circle,solve
from plotting.plots import fire_plot,case_plot,equation_plot
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
 time_s=np.arange(0,DURATION_MIN*60+DT_S,DT_S);sc=scenarios();fire_png=PNG_DIR/'01_courbes_feu.png';eq_png=PNG_DIR/'00_formules.png';fire_plot(time_s/60,sc,fire_png);equation_plot(eq_png)
 allcases=[];rows=[]
 for s in sc:
  for p in POSITIONS:
   for hf in FLAME_HEIGHTS:
    df,g,m=run_case(s,p,hf,time_s);stem=f'{s.code}_{p.code}_H{int(hf)}';df.to_csv(CSV_DIR/f'{stem}.csv',sep=';',decimal=',',index=False);png=PNG_DIR/f'{stem}.png';case_plot(df,f'{s.label} - {p.label} - H = {hf:.0f} m',png)
    allcases.append((stem,s,p,hf,df,g,m,png));rows.append({'Cas':stem,'Tmax intrados (°C)':round(df.T_deck.max(),1),'Tmax suspente (°C)':round(df.T_hanger.max(),1),'Tmax câble (°C)':round(df.T_cable.max(),1)})
 summary=pd.DataFrame(rows);summary.to_csv(CSV_DIR/'SYNTHESE.csv',sep=';',decimal=',',index=False)
 # Sélection worst case à exactement 30 min sur tous les éléments et cas
 idx=int(round(30*60/DT_S));candidates=[]
 for stem,s,p,hf,df,g,m,png in allcases:
  for element in ('deck','hanger','cable'):candidates.append((float(df.loc[idx,f'T_{element}']),stem,s,p,hf,df,m[element],png,element))
 _,stem,s,p,hf,df,me,png,element=max(candidates,key=lambda x:x[0]);i=idx
 worst={'case':stem,'fire':s.label,'position':p.label,'hf':hf,'element':{'deck':'intrados','hanger':'suspente','cable':'câble principal'}[element],'amv':me['amv'],'fr':me['fr'],'fc':me['fc'],'dt':DT_S,'Tg_start':float(df.loc[i-1,'T_gas']),'T_start':float(df.loc[i-1,f'T_{element}']),'cp':float(df.loc[i,f'cp_{element}']),'qc':float(df.loc[i,f'qc_{element}']),'qr':float(df.loc[i,f'qr_{element}']),'dT':float(df.loc[i,f'dT_{element}']),'T_end':float(df.loc[i,f'T_{element}']),'png':png}
 ctx={'project':[['M7','2 × 3 voies ; 13 + 2 + 12 m'],['Tablier','largeur 7,40 m'],['Intrados minimal','6,125 / 6,900 / 7,250 m'],['Câble principal','câble clos Ø132 mm ; hauteurs 8,120 / 9,400 / 11,070 m'],['Suspentes','ronds Ø42 mm ; entraxe 6,25 m ; naissance à +0,82 m'],['Camion','16 × 2,5 × 4 m'],['Positions du foyer','F1 ouest ; F2 axe M7 ; F3 est'],['Hauteurs d’enveloppe','10 / 12 / 15 m']], 'eq_png':eq_png,'fire_png':fire_png,
 'thermal':[['ρ acier','7 850 kg/m³'],['α_c','25 W/(m²·K)'],['ε_m / ε_f','0,70 / 1,00'],['σ','5,670374419 × 10⁻⁸ W/(m²·K⁴)'],['A_m/V suspente','95,238 m⁻¹'],['A_m/V câble','30,303 m⁻¹'],['A_m/V intrados','100 m⁻¹, provisoire'],['Pas temporel','5 s']],
 'steps':[['1','Calcul de θ_g(t)','Courbe et unités'],['2','Interpolation des hauteurs','F1, F2, F3'],['3','Choix direct/masqué','f_rad et f_conv'],['4','Calcul de c_a(θ_a)','Loi acier par morceaux'],['5','Calcul q_conv et q_rad','Flux en W/m²'],['6','Calcul de Δθ_a','Bilan énergétique'],['7','Mise à jour de θ_a','CSV et courbes'],['8','Extraction à 30 min','Cas le plus défavorable']], 'summary':summary,'worst':worst,
 'conclusions':['Les formules de feu sont affichées sous forme d’équations lisibles, indépendantes des limitations typographiques de Word.','Le rapport est entièrement rédigé en français avec accents et unités SI.','Le cas le plus défavorable à 30 min est sélectionné automatiquement parmi les 18 cas et les trois familles d’éléments.','Le dernier pas de calcul avant 30 min est détaillé avec température gaz, température acier, chaleur spécifique, flux convectif, flux radiatif et incrément de température.','Les coefficients d’exposition et le facteur de massiveté de l’intrados restent à justifier avant utilisation en dimensionnement.']}
 out=REPORT_DIR/REPORT_FILENAME
 if GENERATE_REPORT:build_report(ctx,out);print(f'[OK] Rapport généré : {out.resolve()}')
 print(f"[OK] Worst case 30 min : {worst['case']} / {worst['element']} / {worst['T_end']:.2f} °C")
if __name__=='__main__':main()
