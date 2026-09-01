from pathlib import Path
import numpy as np
import pandas as pd
from data.assumptions import *
from data.project_data import BridgeGeometry, TRUCK_POSITIONS
from models.fires import default_fire_scenarios
from models.geometry import case_geometry, geometric_exposure
from models.thermal import LumpedSteelElement, circular_section_factor, integrate_lumped_temperature
from models.materials import steel_strength_reduction, steel_stiffness_reduction
from plotting.plots import plot_fire_curves, plot_case, plot_envelope
from reporting.report import create_word_report

def first_crossing(time_min, values, threshold):
    idx=np.flatnonzero(values>=threshold)
    return None if len(idx)==0 else float(time_min[idx[0]])

def run_case(fire, position, flame_height_m, time_s):
    bridge=BridgeGeometry(); time_min=time_s/60.; tg=fire.gas_temperature_c(time_min)
    geom=case_geometry(position,flame_height_m)
    deck_vf=geometric_exposure(geom["deck_height_m"],flame_height_m,DECK_VIEW_FACTOR,0.30)
    hanger_vf=geometric_exposure(geom["hanger_height_m"],flame_height_m,NEAR_HANGER_VIEW_FACTOR,MASKED_HANGER_VIEW_FACTOR)
    cable_vf=geometric_exposure(geom["cable_height_m"],flame_height_m,NEAR_CABLE_VIEW_FACTOR,MASKED_CABLE_VIEW_FACTOR)
    elements={
      "deck":LumpedSteelElement("Intrados",100.0,deck_vf), # V1.1 placeholder: update from exposed plate geometry
      "hanger":LumpedSteelElement("Suspente",circular_section_factor(bridge.hanger_diameter_m),hanger_vf),
      "cable":LumpedSteelElement("Cable principal",circular_section_factor(bridge.main_cable_diameter_m),cable_vf),
    }
    data={"time_min":time_min,"T_gas_C":tg}
    for key,element in elements.items():
        temp,qc,qr=integrate_lumped_temperature(time_s,tg,element)
        data[f"T_{key}_C"]=temp; data[f"qconv_{key}_W_m2"]=qc; data[f"qrad_{key}_W_m2"]=qr
    df=pd.DataFrame(data)
    df["ky_hanger"]=steel_strength_reduction(df["T_hanger_C"]); df["kE_hanger"]=steel_stiffness_reduction(df["T_hanger_C"])
    meta={"fire":fire.code,"position":position.code,"flame_height_m":flame_height_m,**geom,"view_factor_deck":deck_vf,"view_factor_hanger":hanger_vf,"view_factor_cable":cable_vf}
    return df,meta

def print_case(df,meta):
    print("\n"+"="*72); print(f'{meta["fire"]} | {meta["position"]} | flamme {meta["flame_height_m"]:.0f} m')
    print(f'Hauteurs: intrados={meta["deck_height_m"]:.3f} m, suspente={meta["hanger_height_m"]:.3f} m, cable={meta["cable_height_m"]:.3f} m')
    for c,label in [("T_deck_C","Intrados"),("T_hanger_C","Suspente"),("T_cable_C","Cable")]:
        print(f'{label:10s}: Tmax={df[c].max():7.1f} degC',end="")
        times=[first_crossing(df["time_min"].values,df[c].values,seuil) for seuil in TEMPERATURE_THRESHOLDS_C]
        print(" | seuils " + ", ".join(f'{s}C={"-" if t is None else f"{t:.1f} min"}' for s,t in zip(TEMPERATURE_THRESHOLDS_C,times)))

def main():
    for d in (PNG_DIR,CSV_DIR,REPORT_DIR,LOG_DIR): d.mkdir(parents=True,exist_ok=True)
    scenarios=default_fire_scenarios(); time_s=np.arange(0,SIM_DURATION_MIN*60+TIME_STEP_SEC,TIME_STEP_SEC,dtype=float); time_min=time_s/60.
    if SAVE_PNG: plot_fire_curves(time_min,scenarios,PNG_DIR/"01_courbes_feu.png",SHOW_PLOTS)
    cases=[]; summaries=[]; pngs=[PNG_DIR/"01_courbes_feu.png"]
    for fire in scenarios:
      for pos in TRUCK_POSITIONS:
       for h in FLAME_HEIGHTS_M:
        df,meta=run_case(fire,pos,h,time_s); stem=f'{fire.code}_{pos.code}_H{int(h)}'
        df.to_csv(CSV_DIR/f'{stem}.csv',index=False,sep=';',decimal=',')
        if SAVE_PNG:
            p=PNG_DIR/f'{stem}.png'; plot_case(df,f'{fire.label} - {pos.label} - H={h:.0f} m',p,SHOW_PLOTS); pngs.append(p)
        if VERBOSE: print_case(df,meta)
        cases.append((stem,df,meta))
        summaries.append({"Cas":stem,"Tmax_intrados_C":round(df.T_deck_C.max(),1),"Tmax_suspente_C":round(df.T_hanger_C.max(),1),"Tmax_cable_C":round(df.T_cable_C.max(),1)})
    env=pd.DataFrame({"time_min":time_min})
    for col in ("T_deck_C","T_hanger_C","T_cable_C"): env[col]=np.maximum.reduce([d[col].values for _,d,_ in cases])
    env.to_csv(CSV_DIR/"ENVELOPPE.csv",index=False,sep=';',decimal=',')
    ep=PNG_DIR/"99_enveloppe.png"; plot_envelope(env,ep,SHOW_PLOTS); pngs.append(ep)
    summary=pd.DataFrame(summaries); summary.to_csv(CSV_DIR/"SYNTHESE.csv",index=False,sep=';',decimal=',')
    print("\nCAS ENVELOPPES PAR ELEMENT")
    for col in ("Tmax_intrados_C","Tmax_suspente_C","Tmax_cable_C"):
        row=summary.loc[summary[col].idxmax()]; print(f'{col}: {row["Cas"]} -> {row[col]} degC')
    if GENERATE_REPORT: create_word_report(summary,pngs,REPORT_DIR/"Rapport_V1_1.docx")

if __name__=="__main__": main()
