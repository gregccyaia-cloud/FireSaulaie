import numpy as np,matplotlib.pyplot as plt
COL={'F1':'tab:blue','F2':'tab:orange','F3':'tab:green'}
def save(f,p):f.tight_layout();f.savefig(p,dpi=190,bbox_inches='tight');plt.close(f)
def fireplot(tm,curves,p):
 f,a=plt.subplots(figsize=(8,4.5));[a.plot(tm,y,lw=2,label=k) for k,y in curves.items()];a.set(title='Courbes nominales température-temps',xlabel='Temps (min)',ylabel='Température des gaz (°C)');a.grid(alpha=.3);a.legend();save(f,p)
def family(cases,el,L,p,title):
 f,a=plt.subplots(figsize=(8.5,4.7))
 for c in cases:
  if c['L']==L:a.plot(c['tm'],c[el],color=COL[c['pos']],ls='--' if c['fire']=='ISO 834' else '-',lw=2,label=c['fire']+' - '+c['pos'])
 a.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');a.grid(alpha=.3);a.legend(ncol=2,fontsize=8);save(f,p)
def envelope(cases,fire,el,p,title):
 f,a=plt.subplots(figsize=(8.5,4.7));s=[c for c in cases if c['fire']==fire];Y=np.vstack([c[el] for c in s]);tm=s[0]['tm']
 for c in s:a.plot(tm,c[el],color=COL[c['pos']],lw=.75,alpha=.4,label=f"{c['pos']}-{c['L']:g}m")
 a.fill_between(tm,Y.min(0),Y.max(0),color='.75',alpha=.5,label='Domaine min.-max.');a.plot(tm,Y.max(0),'k',lw=2.2,label='Enveloppe maximale');a.set(title=title,xlabel='Temps (min)',ylabel='Température (°C)');a.grid(alpha=.3);a.legend(ncol=3,fontsize=7);save(f,p)
