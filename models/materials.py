import numpy as np

def steel_specific_heat_j_kgk(theta_c):
    # EN 1993-1-2 piecewise model for carbon steel.
    t=np.asarray(theta_c, dtype=float)
    cp=np.empty_like(t)
    m1=(t>=20)&(t<600); m2=(t>=600)&(t<735); m3=(t>=735)&(t<900); m4=t>=900
    cp[m1]=425+7.73e-1*t[m1]-1.69e-3*t[m1]**2+2.22e-6*t[m1]**3
    cp[m2]=666+13002/(738-t[m2])
    cp[m3]=545+17820/(t[m3]-731)
    cp[m4]=650
    cp[t<20]=425
    return cp if cp.ndim else float(cp)

_TEMP=np.array([20,100,200,300,400,500,600,700,800,900,1000,1100,1200],float)
_KY=np.array([1,1,1,1,1,0.78,0.47,0.23,0.11,0.06,0.04,0.02,0],float)
_KE=np.array([1,1,0.9,0.8,0.7,0.6,0.31,0.13,0.09,0.0675,0.045,0.0225,0],float)

def steel_strength_reduction(theta_c): return np.interp(theta_c,_TEMP,_KY)
def steel_stiffness_reduction(theta_c): return np.interp(theta_c,_TEMP,_KE)
