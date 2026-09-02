import numpy as np
def iso(t):return 20+345*np.log10(8*np.asarray(t)+1)
def ext(t):
 t=np.asarray(t);return 660*(1-.687*np.exp(-.32*t)-.313*np.exp(-3.8*t))+20
CURVES={'ISO 834':iso,'Feu extérieur':ext}
