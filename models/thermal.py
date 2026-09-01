import numpy as np
from data.assumptions import RHO,EMISSIVITY,FIRE_EMISSIVITY,ALPHA_C,SIGMA
from models.materials import cp_steel
def section_factor(d): return 4/d
def solve(time_s,tg,amv,vf):
 T=np.empty_like(time_s); T[0]=20.
 for i in range(1,len(T)):
  dt=time_s[i]-time_s[i-1]; a=T[i-1]; g=tg[i-1]
  qc=ALPHA_C*(g-a); qr=vf*EMISSIVITY*FIRE_EMISSIVITY*SIGMA*((g+273.15)**4-(a+273.15)**4)
  T[i]=min(a+amv*(qc+qr)*dt/(RHO*cp_steel(a)),tg[i])
 return T
