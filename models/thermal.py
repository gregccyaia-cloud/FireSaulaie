import numpy as np
from data.config import *
from models.material import cp_steel
def amv_circle(d):return 4./d
def fluxes(tg,ta,fr,fc):
 qc=fc*ALPHA_C*(tg-ta);qr=fr*EPS_M*EPS_F*SIGMA*((tg+273.15)**4-(ta+273.15)**4);return qc,qr
def solve(time_s,tg,amv,fr,fc):
 T=np.empty_like(time_s,dtype=float);qc=np.zeros_like(T);qr=np.zeros_like(T);cp=np.zeros_like(T);dT=np.zeros_like(T);T[0]=T0;cp[0]=cp_steel(T0)
 for i in range(1,len(T)):
  dt=time_s[i]-time_s[i-1];cp[i]=cp_steel(T[i-1]);qc[i],qr[i]=fluxes(tg[i-1],T[i-1],fr,fc);dT[i]=amv*(qc[i]+qr[i])*dt/(RHO*cp[i]);T[i]=min(T[i-1]+dT[i],tg[i])
 return T,qc,qr,cp,dT
