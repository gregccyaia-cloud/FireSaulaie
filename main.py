import numpy as np,pandas as pd
from data.assumptions import *
from data.project_data import *
from models.fires import scenarios
from models.geometry import geometry,exposure_key,_quad
from models.thermal import section_factor_circle,solve
from plotting.plots import fire_curves,case,geometry_profile,convergence
from reporting.report import create_report

def run(dt=TIME_STEP_SEC):
 ts=np.arange(0,SIM_DURATION_MIN*60+dt,dt);tm=ts/60;out=[]
 for s in scenarios():
  for p in POSITIONS:
   for hf in FLAME_HEIGHTS_M:
    g=geometry(p,hf);tg=s.temperature(tm);frames={'time_min':tm,'T_gas_C':tg}
    specs=[('deck',DECK_SECTION_FACTOR_M_1,g['h_deck_m']),('hanger',section_factor_circle(HANGER_DIAMETER_M),g['h_hanger_m']),('cable',section_factor_circle(CABLE_DIAMETER_M),g['h_cable_m'])]
    for name,amv,h in specs:
     key=exposure_key(name,h,hf);fr,fc=EXPOSURE[key];T,qc,qr=solve(ts,tg,amv,fr,fc);frames[f'T_{name}_C']=T;frames[f'qconv_{name}_W_m2']=qc;frames[f'qrad_{name}_W_m2']=qr
    out.append((f'{s.code}_{p.code}_H{int(hf)}',pd.DataFrame(frames),g,s,p,hf))
 return out

def main():
 for d in (PNG_DIR,CSV_DIR,REPORT_DIR,LOG_DIR):d.mkdir(parents=True,exist_ok=True)
 sc=scenarios(); fire_png=PNG_DIR/'01_courbes_feu.png';fire_curves(np.linspace(0,120,721),sc,fire_png)
 xs=np.linspace(0,27,200);deck=np.array([_quad(x,H_DECK) for x in xs]);cable=np.array([_quad(x,H_CABLE) for x in xs]);geom_png=PNG_DIR/'02_geometrie.png';geometry_profile(xs,deck,cable,geom_png)
 cases=run(); rows=[]; figs=[]
 for stem,df,g,s,p,hf in cases:
  df.to_csv(CSV_DIR/f'{stem}.csv',sep=';',decimal=',',index=False)
  png=PNG_DIR/f'{stem}.png';case(df,f'{s.label} - {p.label} - H={hf:.0f} m',png);figs.append((png,f'{stem} : evolution des temperatures.'))
  rows.append({'Cas':stem,'Tmax intrados':round(df.T_deck_C.max(),1),'Tmax suspente':round(df.T_hanger_C.max(),1),'Tmax cable':round(df.T_cable_C.max(),1)})
 summary=pd.DataFrame(rows);summary.to_csv(CSV_DIR/'SYNTHESE.csv',sep=';',decimal=',',index=False)
 # convergence on a representative severe case
 c5=next(x for x in cases if x[0]=='ISO834_F1_H15')[1];c25=next(x for x in run(2.5) if x[0]=='ISO834_F1_H15')[1]
 interp=np.interp(c5.time_min,c25.time_min,c25.T_hanger_C);err=float(np.max(np.abs(c5.T_hanger_C-interp)));conv_png=PNG_DIR/'03_convergence.png';convergence(c5.time_min,c5.T_hanger_C,interp,conv_png)
 ctx={'project_rows':[['M7','2 x 3 voies, largeur simplifiee 13 + 2 + 12 m'],['Tablier','largeur 7,40 m'],['Hauteurs intrados','6,125 / 6,900 / 7,250 m'],['Hauteurs axe cable','8,120 / 9,400 / 11,070 m'],['Suspentes','rond 42 mm, entraxe 6,25 m'],['Cable principal','cable clos 132 mm, acier nu'],['Camion','16 x 2,5 x 4 m'],['Positions','F1 ouest, F2 axe M7, F3 est'],['Enveloppes de flamme','10 / 12 / 15 m']],
 'geometry_png':geom_png,'fire_png':fire_png,'conv_png':conv_png,
 'fire_rows':[['ISO 834','20 + 345 log10(8t + 1)','0 a 120 min'],['Feu exterieur CEREMA','660(1 - 0,687 exp(-0,32t) - 0,313 exp(-3,8t)) + 20','0 a 120 min']],
 'thermal_rows':[['rho acier','7 850 kg/m3','normatif'],['alpha_c direct','25 W/m2.K','hypothese normative courante'],['epsilon acier','0,70','hypothese normative courante'],['epsilon feu','1,00','hypothese normative courante'],['pas temporel','5 s','valide par controle numerique'],['A_m/V suspente','95,24 m-1','geometrie fournie'],['A_m/V cable','30,30 m-1','geometrie fournie'],['A_m/V intrados','100 m-1','provisoire'],['coefficients exposition','0,15 a 1,00','depistage, a justifier']],
 'steps_rows':[['1','Construction du vecteur temps','0 a 120 min, pas 5 s'],['2','Calcul theta_g(t)','courbe de gaz par scenario'],['3','Interpolation parabolique des hauteurs','hauteurs locales F1/F2/F3'],['4','Choix exposition directe ou masquee','f_rad et f_conv'],['5','Calcul q_conv et q_rad','W/m2 a chaque pas'],['6','Integration du bilan thermique','temperature acier'],['7','Extraction des maxima et temps intermediaires','CSV, console, graphiques'],['8','Comparaison de tous les cas','enveloppe finale']],
 'validation_text':f'Le controle de convergence compare le pas nominal de 5 s a un pas de 2,5 s sur ISO834_F1_H15. L ecart absolu maximal sur la temperature de la suspente est de {err:.3f} degC. Ce controle valide la discretisation temporelle pour le modele retenu, mais ne valide pas les coefficients d exposition ni la representation spatiale de la flamme.',
 'summary':summary,'case_figures':[figs[0],figs[8],figs[9],figs[-1]],
 'conclusions':['Les equations de courbes de feu, le bilan convection-rayonnement, la chaleur specifique variable et les facteurs de massiveté sont explicitement traces dans le code et le rapport.','La convergence temporelle est controlee automatiquement.','La validation physique reste partielle : les coefficients d exposition et le facteur de massiveté de l intrados sont provisoires.','Les temperatures des elements en exposition masquee doivent etre considerees comme des valeurs de depistage, non comme des valeurs de dimensionnement.','Le passage a un feu localise de l EN 1991-1-2 annexe C requiert Q(t), le diametre equivalent du foyer et la position geometrique detaillee.']}
 out=REPORT_DIR/REPORT_NAME;create_report(ctx,out);print(f'Rapport genere: {out.resolve()} ({out.stat().st_size} octets)');print(f'Ecart convergence max: {err:.3f} degC')
if __name__=='__main__':main()
