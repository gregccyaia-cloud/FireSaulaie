import numpy as np
from data.assumptions import *
from models.materials import cp_steel
def section_factor_circle(d):return 4./d
def fluxes(tg,ta,rad_factor,conv_factor):
 qc=conv_factor*ALPHA_C_DIRECT*(tg-ta)
 qr=rad_factor*EPS_STEEL*EPS_FIRE*SIGMA*((tg+273.15)**4-(ta+273.15)**4)
 return qc,qr
def solve(time_s,tg,amv,rad_factor,conv_factor):
 T=np.empty_like(time_s,dtype=float); qc=np.zeros_like(T); qr=np.zeros_like(T); T[0]=T0_C
 for i in range(1,len(T)):
  dt=time_s[i]-time_s[i-1]; qc[i],qr[i]=fluxes(tg[i-1],T[i-1],rad_factor,conv_factor)
  T[i]=T[i-1]+amv*(qc[i]+qr[i])*dt/(RHO_STEEL*cp_steel(T[i-1]))
  T[i]=min(T[i],tg[i])
 return T,qc,qr
