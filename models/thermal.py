from dataclasses import dataclass
import numpy as np
from data.assumptions import (INITIAL_TEMPERATURE_C, STEEL_DENSITY_KG_M3, STEEL_EMISSIVITY, FIRE_EMISSIVITY, CONVECTION_COEFF_W_M2K, STEFAN_BOLTZMANN)
from models.materials import steel_specific_heat_j_kgk

@dataclass(frozen=True)
class LumpedSteelElement:
    name: str
    section_factor_m_1: float
    view_factor: float
    convection_factor: float = 1.0
    shadow_factor: float = 1.0

def circular_section_factor(diameter_m: float) -> float:
    return 4.0/diameter_m

def heat_fluxes_w_m2(t_gas_c, t_steel_c, view_factor, convection_factor=1.0):
    q_conv=convection_factor*CONVECTION_COEFF_W_M2K*(t_gas_c-t_steel_c)
    tg=t_gas_c+273.15; ts=t_steel_c+273.15
    q_rad=view_factor*STEEL_EMISSIVITY*FIRE_EMISSIVITY*STEFAN_BOLTZMANN*(tg**4-ts**4)
    return q_conv, q_rad

def integrate_lumped_temperature(time_s, gas_temp_c, element):
    temp=np.empty_like(time_s,dtype=float); temp[0]=INITIAL_TEMPERATURE_C
    qconv=np.zeros_like(time_s,dtype=float); qrad=np.zeros_like(time_s,dtype=float)
    for i in range(1,len(time_s)):
        dt=time_s[i]-time_s[i-1]
        qc,qr=heat_fluxes_w_m2(gas_temp_c[i-1],temp[i-1],element.view_factor,element.convection_factor)
        cp=steel_specific_heat_j_kgk(temp[i-1])
        dtheta=element.shadow_factor*element.section_factor_m_1*(qc+qr)*dt/(STEEL_DENSITY_KG_M3*cp)
        temp[i]=min(temp[i-1]+dtheta, gas_temp_c[i])
        qconv[i]=qc; qrad[i]=qr
    return temp,qconv,qrad
