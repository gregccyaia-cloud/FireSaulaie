import numpy as np
class ISO834:
 code='ISO834'; label='ISO 834'; reference='EN 1991-1-2, courbe nominale standard'
 def temperature(self,t_min): return 20.+345.*np.log10(8.*np.asarray(t_min,dtype=float)+1.)
class CeremaExternal:
 code='CEREMA_EXT'; label='Feu exterieur CEREMA'; reference='Guide CEREMA 2018, formule fournie au projet'
 def temperature(self,t_min):
  t=np.asarray(t_min,dtype=float); return 660.*(1.-.687*np.exp(-.32*t)-.313*np.exp(-3.8*t))+20.
def scenarios(): return (ISO834(),CeremaExternal())
