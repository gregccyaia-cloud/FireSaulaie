import numpy as np
from data.config import *
from models.material import cp_steel
def amv(d):return 4./d
def phi_rectangle(length_m,receiver_height_m,truck_height_m=4.):
 # Facteur géométrique de sensibilité : rectangle centré vu depuis un point.
 # Borne supérieure 1.0. À valider par un modèle de flamme plus abouti.
 h=max(receiver_height_m-truck_height_m,.25)
 return float(np.clip((2./np.pi)*np.arctan(length_m/(2.*h)),0.,1.))
def solve(time_s,tg,diameter,phi,conv_factor=1.):
 T=np.empty_like(time_s,float);qc=np.zeros_like(T);qr=np.zeros_like(T);cp=np.zeros_like(T);inc=np.zeros_like(T);T[0]=T0;A=amv(diameter)
 for i in range(1,len(T)):
  dt=time_s[i]-time_s[i-1];cp[i]=cp_steel(T[i-1]);qc[i]=conv_factor*ALPHA_C*(tg[i-1]-T[i-1]);qr[i]=phi*EPS_M*EPS_F*SIGMA*((tg[i-1]+273.15)**4-(T[i-1]+273.15)**4);inc[i]=K_SH*A*(qc[i]+qr[i])*dt/(RHO*cp[i]);T[i]=min(T[i-1]+inc[i],tg[i])
 return T,qc,qr,cp,inc
