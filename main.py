import numpy as np, pandas as pd
from data.assumptions import *
from data.project_data import POSITIONS,HANGER_D,CABLE_D
from models.fires import scenarios
from models.geometry import geometry,exposure
from models.thermal import section_factor,solve
from plotting.plots import case_plot,fire_plot
from reporting.report import create_report

def main():
 for d in (PNG_DIR,CSV_DIR,REPORT_DIR):d.mkdir(parents=True,exist_ok=True)
 ts=np.arange(0,SIM_DURATION_MIN*60+TIME_STEP_SEC,TIME_STEP_SEC);tm=ts/60;ss=scenarios();pngs=[];rows=[]
 fp=PNG_DIR/'01_courbes_feu.png';fire_plot(tm,ss,fp);pngs.append(fp)
 for s in ss:
  for p in POSITIONS:
   for hf in FLAME_HEIGHTS_M:
    g=geometry(p,hf);tg=s.temperature(tm)
    vd=exposure(g['h_deck'],hf,VF_DECK,.3);vh=exposure(g['h_hanger'],hf,VF_HANGER_DIRECT,VF_HANGER_MASKED);vc=exposure(g['h_cable'],hf,VF_CABLE_DIRECT,VF_CABLE_MASKED)
    df=pd.DataFrame({'time_min':tm,'T_gas':tg,'T_deck':solve(ts,tg,100.,vd),'T_hanger':solve(ts,tg,section_factor(HANGER_D),vh),'T_cable':solve(ts,tg,section_factor(CABLE_D),vc)})
    stem=f'{s.code}_{p.code}_H{int(hf)}';df.to_csv(CSV_DIR/f'{stem}.csv',sep=';',decimal=',',index=False)
    pp=PNG_DIR/f'{stem}.png';case_plot(df,f'{s.label} - {p.label} - H={hf:.0f} m',pp,SHOW_PLOTS);pngs.append(pp)
    rows.append({'Cas':stem,'Tmax intrados':round(df.T_deck.max(),1),'Tmax suspente':round(df.T_hanger.max(),1),'Tmax cable':round(df.T_cable.max(),1)})
    if VERBOSE:print(stem,rows[-1])
 summary=pd.DataFrame(rows);summary.to_csv(CSV_DIR/'SYNTHESE.csv',sep=';',decimal=',',index=False)
 report=REPORT_DIR/'Rapport_V1_1.docx'
 if GENERATE_REPORT:
  print(f'Generation du rapport : {report.resolve()}');create_report(summary,pngs,report)
  if not report.exists() or report.stat().st_size==0:raise RuntimeError(f'Rapport non cree: {report}')
  print(f'Rapport genere avec succes ({report.stat().st_size} octets).')
 else:print('Rapport desactive: GENERATE_REPORT=False')
if __name__=='__main__':main()
