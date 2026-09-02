import numpy as np
TH=np.array([20.,100.,200.,300.,400.,500.,600.,700.,800.,900.,1000.,1100.,1200.]);KY=np.array([1.,1.,1.,1.,1.,.78,.47,.23,.11,.06,.04,.02,0.])
def ky(theta):return np.interp(np.asarray(theta,float),TH,KY,left=1.,right=0.)
def ft_theta(ft20,theta):return float(ft20)*ky(theta)
