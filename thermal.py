from dataclasses import dataclass
import numpy as np
from config import *
def cp_steel(x):
 t=max(20.,float(x))
 if t<600:return 425.+.773*t-.00169*t*t+2.22e-6*t**3
 if t<735:return 666.+13002./(738.-t)
 if t<900:return 545.+17820./(t-731.)
 return 650.
@dataclass
class History:t:np.ndarray;tg:np.ndarray;ta:np.ndarray;qc:np.ndarray;qr:np.ndarray;qn:np.ndarray;cp:np.ndarray;dta:np.ndarray
def integrate(t,tg,amv):
 n=len(t);ta=np.full(n,AMBIENT_C);qc=np.zeros(n);qr=np.zeros(n);qn=np.zeros(n);cp=np.zeros(n);dt=np.zeros(n);cp[0]=cp_steel(ta[0])
 for i in range(1,n):
  cp[i]=cp_steel(ta[i-1]);qc[i]=ALPHA_C*(tg[i]-ta[i-1]);qr[i]=PHI*EPSILON_M*EPSILON_F*SIGMA*((tg[i]+273.15)**4-(ta[i-1]+273.15)**4);qn[i]=qc[i]+qr[i];dt[i]=K_SH*amv*qn[i]*DT_SECONDS/(RHO_STEEL*cp[i]);ta[i]=min(tg[i],ta[i-1]+dt[i])
 return History(t,tg,ta,qc,qr,qn,cp,dt)
