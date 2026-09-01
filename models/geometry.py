import numpy as np
from data.project_data import X,H_DECK,H_CABLE,HANGER_DZ
def _q(x,z): return float(np.polyval(np.polyfit(X,z,2),x))
def geometry(position,hflame):
 hd=_q(position.x,H_DECK); hc=_q(position.x,H_CABLE)
 return {'x':position.x,'h_deck':hd,'h_hanger':hd+HANGER_DZ,'h_cable':hc,'h_flame':hflame}
def exposure(h,hflame,direct,masked): return direct if h<=hflame else masked
