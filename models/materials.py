import numpy as np
def cp_steel(theta):
 t=float(theta)
 if t<600:return 425+.773*t-.00169*t*t+2.22e-6*t**3
 if t<735:return 666+13002/(738-t)
 if t<900:return 545+17820/(t-731)
 return 650.
T=np.array([20,100,200,300,400,500,600,700,800,900,1000,1100,1200.]); KY=np.array([1,1,1,1,1,.78,.47,.23,.11,.06,.04,.02,0]); KE=np.array([1,1,.9,.8,.7,.6,.31,.13,.09,.0675,.045,.0225,0])
def ky(t):return np.interp(t,T,KY)
def kE(t):return np.interp(t,T,KE)
