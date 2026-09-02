import numpy as np
def iso834(t): t=np.asarray(t,float); return 20.+345.*np.log10(8.*t+1.)
def external_fire(t): t=np.asarray(t,float); return 660.*(1.-.687*np.exp(-.32*t)-.313*np.exp(-3.8*t))+20.
CURVES={'Feu 1 - ISO 834':iso834,'Feu 2 - Feu extérieur':external_fire}
