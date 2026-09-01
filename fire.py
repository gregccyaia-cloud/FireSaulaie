import numpy as np
def iso834(t):
    """NF EN 1991-1-2 § 3.2.1 ; guide Cerema 2018."""
    t=np.asarray(t,float); return 20.+345.*np.log10(8.*t+1.)
def external_fire(t):
    """NF EN 1991-1-2 § 3.2.2 ; guide Cerema 2018."""
    t=np.asarray(t,float); return 660.*(1.-.687*np.exp(-.32*t)-.313*np.exp(-3.8*t))+20.
CURVES={'ISO 834':iso834,'Feu extérieur':external_fire}
