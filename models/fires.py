import numpy as np
class ISO834:
 code='ISO834'; label='ISO 834'
 def temperature(self,t): return 20+345*np.log10(8*np.asarray(t)+1)
class CeremaExternal:
 code='CEREMA_EXT'; label='Feu exterieur CEREMA'
 def temperature(self,t):
  t=np.asarray(t); return 660*(1-.687*np.exp(-.32*t)-.313*np.exp(-3.8*t))+20
def scenarios(): return (ISO834(),CeremaExternal())
