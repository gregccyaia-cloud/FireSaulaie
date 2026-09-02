import numpy as np
from config import *
def gas(t,kind):
 t=np.asarray(t,float)
 if kind=='ISO 834':return 20+345*np.log10(8*t+1)
 if kind=='Feu extérieur':return 660*(1-.687*np.exp(-.32*t)-.313*np.exp(-3.8*t))+20
 if kind=='HC':return 20+1080*(1-.325*np.exp(-.167*t)-.675*np.exp(-2.5*t))
 raise ValueError(kind)
def cp(t):
 t=float(t)
 if t<600:return 425+.773*t-.00169*t*t+2.22e-6*t**3
 if t<735:return 666+13002/(738-t)
 if t<900:return 545+17820/(t-731)
 return 650.
def phi(H,h):
 # Sensibilité géométrique enveloppe liée à la hauteur de flamme H et à la hauteur du récepteur h.
 return float(np.clip(2/np.pi*np.arctan(H/(2*max(h-4,.25))),0,1))
def solve(ts,tg,D,P):
 T=np.full(len(ts),T0);A=4/D
 for i in range(1,len(ts)):
  qc=ALPHA*(tg[i-1]-T[i-1]);qr=P*EPSM*EPSF*SIGMA*((tg[i-1]+273.15)**4-(T[i-1]+273.15)**4);T[i]=min(T[i-1]+KSH*A*(qc+qr)*(ts[i]-ts[i-1])/(RHO*cp(T[i-1])),tg[i])
 return T
TEMP=np.array([20,100,200,300,400,500,600,700,800,900,1000,1100,1200.]);KY=np.array([1,1,1,1,1,.78,.47,.23,.11,.06,.04,.02,0.]);KE=np.array([1,1,.9,.8,.7,.6,.31,.13,.09,.0675,.045,.0225,0.])
def ky(t):return np.interp(t,TEMP,KY)
def ke(t):return np.interp(t,TEMP,KE)
