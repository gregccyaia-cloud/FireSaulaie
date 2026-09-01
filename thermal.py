from dataclasses import dataclass
import numpy as np
from config import *
def cp_steel(theta):
    """NF EN 1993-1-2 §3.4.1.2."""
    t=max(20.,float(theta))
    if t<600: return 425.+.773*t-.00169*t*t+2.22e-6*t**3
    if t<735: return 666.+13002./(738.-t)
    if t<900: return 545.+17820./(t-731.)
    return 650.
def q_conv(tg,ta):
    """q_conv=α_c(θ_g-θ_a), NF EN 1991-1-2 §3.1."""
    return ALPHA_C*(tg-ta)
def q_rad(tg,ta):
    """q_rad=Φε_mε_fσ[(θ_g+273,15)^4-(θ_a+273,15)^4], NF EN 1991-1-2 §3.1."""
    return PHI*EPSILON_M*EPSILON_F*SIGMA*((tg+273.15)**4-(ta+273.15)**4)
@dataclass
class History:
    t:np.ndarray; tg:np.ndarray; ta:np.ndarray; qc:np.ndarray; qr:np.ndarray; qn:np.ndarray; cp:np.ndarray; dta:np.ndarray
def integrate(t,tg,amv):
    """Bilan concentré d'un élément non protégé: NF EN 1993-1-2 §4.2.5.1."""
    n=len(t); ta=np.full(n,AMBIENT_TEMPERATURE_C); qc=np.zeros(n); qr=np.zeros(n); qn=np.zeros(n); cp=np.zeros(n); dta=np.zeros(n); cp[0]=cp_steel(ta[0])
    for i in range(1,n):
        cp[i]=cp_steel(ta[i-1]); qc[i]=q_conv(tg[i],ta[i-1]); qr[i]=q_rad(tg[i],ta[i-1]); qn[i]=qc[i]+qr[i]
        dta[i]=K_SH*amv*qn[i]*DT_SECONDS/(RHO_STEEL*cp[i]); ta[i]=min(tg[i],ta[i-1]+dta[i])
    return History(t,tg,ta,qc,qr,qn,cp,dta)
