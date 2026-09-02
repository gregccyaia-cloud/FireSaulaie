import numpy as np,matplotlib.pyplot as plt
C={'F1':'tab:blue','F2':'tab:orange','F3':'tab:green'}
def save(f,p):f.tight_layout();f.savefig(p,dpi=190,bbox_inches='tight');plt.close(f)
def fire(tm,curves,p):
 f,a=plt.subplots(figsize=(8,4.5));[a.plot(tm,y,lw=2,label=k) for k,y in curves.items()];a.set(title='Courbes nominales température-temps',xlabel='Temps (min)',ylabel='Température des gaz (°C)');a.grid(alpha=.3);a.legend();save(f,p)
def geom(pos,p):
 f,a=plt.subplots(figsize=(8,4.5));x=range(3)
 for key,l in [('deck','Intrados'),('hanger','Naissance suspente'),('cable','Axe câble')]:a.plot(x,[q[key] for q in pos],'o-',label=l)
 a.set_xticks(x,[q['code'] for q in pos]);a.set(title='Trois coupes géométriques de référence et positions F1, F2 et F3',ylabel='Hauteur (m)');a.grid(alpha=.3);a.legend();save(f,p)
def family(cases,element,L,p,title):
 f,a=plt.subplots(figsize=(8.5,4.7))
 for c in cases:
  if c['L']!=L:continue
  a.plot(c['tm'],c[element],color=C[c['pos']],ls='--' if c['fire']=='ISO 834' else '-',lw=2,label=c['fire']+' - '+c['pos'])
 a.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');a.grid(alpha=.3);a.legend(ncol=2,fontsize=8);save(f,p)
def envelope(cases,fire_name,element,p,title):
 f,a=plt.subplots(figsize=(8.5,4.7));sel=[c for c in cases if c['fire']==fire_name];Y=[]
 for c in sel:a.plot(c['tm'],c[element],color=C[c['pos']],lw=.8,alpha=.45,label=f"{c['pos']} - {c['L']:g} m");Y.append(c[element])
 Y=np.vstack(Y);lo=Y.min(0);hi=Y.max(0);tm=sel[0]['tm'];a.fill_between(tm,lo,hi,color='.75',alpha=.5,label='Domaine min.-max.');a.plot(tm,hi,'k',lw=2.3,label='Enveloppe maximale');a.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');a.grid(alpha=.3);a.legend(ncol=3,fontsize=7);save(f,p)
def integration(c,p):
 f,a=plt.subplots(figsize=(8,4.2));a.plot(c['tm'],c['gas'],label='Gaz');a.plot(c['tm'],c['hanger'],label='Suspente');a.axvline(30,color='r',ls='--');a.set(title='Intégration temporelle du cas critique',xlabel='Temps (min)',ylabel='Température (°C)');a.grid(alpha=.3);a.legend();save(f,p)
