import numpy as np
from config import *
def cp(t):
 t=float(t)
 if t<600:return 425+.773*t-.00169*t*t+2.22e-6*t**3
 if t<735:return 666+13002/(738-t)
 if t<900:return 545+17820/(t-731)
 return 650.
def phi(L,h):return float(np.clip(2/np.pi*np.arctan(L/(2*max(h-4,.25))),0,1))
def solve(ts,tg,D,P):
 T=np.full(len(ts),T0);qc=np.zeros(len(ts));qr=np.zeros(len(ts));cv=np.zeros(len(ts));di=np.zeros(len(ts));A=4/D
 for i in range(1,len(ts)):
  cv[i]=cp(T[i-1]);qc[i]=ALPHA*(tg[i-1]-T[i-1]);qr[i]=P*EPSM*EPSF*SIGMA*((tg[i-1]+273.15)**4-(T[i-1]+273.15)**4);di[i]=KSH*A*(qc[i]+qr[i])*(ts[i]-ts[i-1])/(RHO*cv[i]);T[i]=min(T[i-1]+di[i],tg[i])
 return T,qc,qr,cv,di
# Facteur de réduction du module d'Young par interpolation des valeurs tabulées EC3
TEMP=np.array([20,100,200,300,400,500,600,700,800,900,1000,1100,1200.],float)
KE=np.array([1,1,.9,.8,.7,.6,.31,.13,.09,.0675,.045,.0225,0.],float)
def kE(theta):return float(np.interp(float(theta),TEMP,KE))
