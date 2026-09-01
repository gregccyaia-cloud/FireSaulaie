import numpy as np
def iso834(t):
    """θ_g=20+345log10(8t+1), NF EN 1991-1-2 §3.2.1."""
    t=np.asarray(t,float); return 20.+345.*np.log10(8.*t+1.)
def external_fire(t):
    """θ_g=660[1-0,687e^-0,32t-0,313e^-3,8t]+20, NF EN 1991-1-2 §3.2.2."""
    t=np.asarray(t,float); return 660.*(1.-.687*np.exp(-.32*t)-.313*np.exp(-3.8*t))+20.
CURVES={'ISO 834':iso834,'Feu extérieur':external_fire}
