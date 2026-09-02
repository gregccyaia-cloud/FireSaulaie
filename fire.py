"""Courbes nominales de la NF EN 1991-1-2."""
import numpy as np
def iso834(t):
    """Courbe normalisée, §3.2.1."""; t=np.asarray(t,float); return 20.+345.*np.log10(8.*t+1.)
def external_fire(t):
    """Courbe de feu extérieur, §3.2.2."""; t=np.asarray(t,float); return 660.*(1.-.687*np.exp(-.32*t)-.313*np.exp(-3.8*t))+20.
def hydrocarbon_fire(t):
    """Courbe hydrocarbure HC non majorée, §3.2.3.
    θ_g(t)=1080(1-0,325e^(-0,167t)-0,675e^(-2,5t))+20, t en min.
    """; t=np.asarray(t,float); return 1080.*(1.-.325*np.exp(-.167*t)-.675*np.exp(-2.5*t))+20.
CURVES={'Feu 1 - CN ISO 834':iso834,'Feu 2 - Feu extérieur':external_fire,'Feu 3 - Hydrocarbure HC':hydrocarbon_fire}
