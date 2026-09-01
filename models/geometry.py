import numpy as np
from data.project import *
def q(x,z):return float(np.polyval(np.polyfit(X,z,2),x))
def geometry(p,hf):
 hd=q(p.x_m,H_DECK);hc=q(p.x_m,H_CABLE)
 return {'x_m':p.x_m,'h_flame_m':hf,'h_deck_m':hd,'h_hanger_m':hd+HANGER_DZ,'h_cable_m':hc}
def key(element,h,hf):
 if element=='deck':return 'deck'
 return element+'_direct' if h<=hf else element+'_masked'
