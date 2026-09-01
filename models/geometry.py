import numpy as np
from data.project_data import *
def _quad(x,z): return float(np.polyval(np.polyfit(X_STATIONS,z,2),x))
def intrados_rise(y):
 y=abs(float(y))
 if y>DECK_HALF_WIDTH_M: raise ValueError('y hors tablier')
 if y<=PROFILE_BREAK_Y_M:return PROFILE_BREAK_RISE_M*y/PROFILE_BREAK_Y_M
 return PROFILE_BREAK_RISE_M+(EDGE_RISE_M-PROFILE_BREAK_RISE_M)*(y-PROFILE_BREAK_Y_M)/(DECK_HALF_WIDTH_M-PROFILE_BREAK_Y_M)
def geometry(p,hf):
 hd=_quad(p.x_m,H_DECK); hc=_quad(p.x_m,H_CABLE)
 return {'x_m':p.x_m,'h_flame_m':hf,'h_deck_m':hd,'h_hanger_m':hd+HANGER_LOWER_DZ_M,'h_cable_m':hc}
def exposure_key(element,h,hf):
 if element=='deck': return 'deck'
 return f'{element}_direct' if h<=hf else f'{element}_masked'
