from pathlib import Path
import matplotlib.pyplot as plt
COL={'F1':'tab:blue','F2':'tab:orange','F3':'tab:green'};LS={10.:'-',15.:'--',20.:':'}
def save(f,p):p=Path(p);f.tight_layout();f.savefig(p,dpi=200,bbox_inches='tight');plt.close(f);return p
def fire_plot(t,d,p):
 f,a=plt.subplots(figsize=(9,5));[a.plot(t,v,lw=2,label=k) for k,v in d.items()];a.set(xlabel='Temps (min)',ylabel='Température des gaz (°C)',title='Courbes nominales température-temps');a.grid();a.legend();return save(f,p)
def curves(t,s,title,ylabel,p):
 f,a=plt.subplots(figsize=(9,5))
 for lab,v,c,L in s:a.plot(t,v,label=lab,color=COL[c],linestyle=LS[L],lw=1.6)
 a.set(xlabel='Temps (min)',ylabel=ylabel,title=title);a.grid();a.legend(fontsize=7,ncol=2);return save(f,p)
def geom(sections,p):
 f,a=plt.subplots(figsize=(9,5));x=range(3);a.plot(x,[s.intrados_m for s in sections],'o-',label='Intrados');a.plot(x,[s.intrados_m+.82 for s in sections],'o-',label='Naissance suspente');a.plot(x,[s.cable_m for s in sections],'o-',label='Axe câble');a.set_xticks(list(x),[s.code for s in sections]);a.set(ylabel='Hauteur (m)',title='Trois coupes géométriques');a.grid();a.legend();return save(f,p)
def integration(h,p):
 m=h.t<=30;f,a=plt.subplots(figsize=(9,5));a.plot(h.t[m],h.tg[m],label='Gaz θg');a.plot(h.t[m],h.ta[m],label='Acier θa');a.set(xlabel='Temps (min)',ylabel='Température (°C)',title="Intégration du cas critique jusqu'à 30 min");a.grid();a.legend();return save(f,p)
