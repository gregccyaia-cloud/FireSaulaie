from pathlib import Path
import numpy as np, matplotlib.pyplot as plt
COL={'F1':'tab:blue','F2':'tab:orange','F3':'tab:green'}
def style(f):return ':' if f.startswith('Feu 1') else ('-' if f.startswith('Feu 2') else '-.')
def save(fig,p):p=Path(p);fig.tight_layout();fig.savefig(p,dpi=210,bbox_inches='tight');plt.close(fig);return p
def fire_plot(t,D,p):
 f,a=plt.subplots(figsize=(9,5));
 for k,v in D.items():a.plot(t,v,lw=2.2,linestyle=style(k),label=k)
 a.set(xlabel='Temps (min)',ylabel='Température des gaz (°C)',title='Comparaison des trois courbes de feu');a.grid();a.legend();return save(f,p)
def grouped(t,S,title,ylabel,p):
 f,a=plt.subplots(figsize=(9,5))
 for fire,code,v in S:a.plot(t,v,color=COL[code],linestyle=style(fire),lw=2,label=f'{fire} - {code}')
 a.set(xlabel='Temps (min)',ylabel=ylabel,title=title);a.grid();a.legend(fontsize=6,ncol=2);return save(f,p)
def envelope(t,C,title,ylabel,p):
 f,a=plt.subplots(figsize=(9,5.3));M=np.vstack([v for _,_,_,v in C]);lo=M.min(0);hi=M.max(0)
 for i,(fire,code,L,v) in enumerate(C):a.plot(t,v,color=COL[code],linestyle=style(fire),lw=.85,alpha=.35,label=f'{fire} - {code} - {int(L)} m',marker={'F1':'o','F2':'s','F3':'^'}[code],markevery=(i*11+10,300),markersize=2.7)
 a.fill_between(t,lo,hi,color='grey',alpha=.22,label='Faisceau min-max des 3 feux');a.plot(t,hi,'k-',lw=2.4,label='Enveloppe supérieure');a.plot(t,lo,'k--',lw=1.5,label='Enveloppe inférieure');a.set(xlabel='Temps (min)',ylabel=ylabel,title=title);a.grid();a.legend(fontsize=5.5,ncol=3);return save(f,p)
def geom(S,p):
 f,a=plt.subplots(figsize=(9,5));x=range(3);a.plot(x,[s.intrados_m for s in S],'o-',label='Intrados');a.plot(x,[s.intrados_m+.82 for s in S],'o-',label='Naissance suspente');a.plot(x,[s.cable_m for s in S],'o-',label='Axe câble');a.set_xticks(list(x),[s.code for s in S]);a.grid();a.legend();return save(f,p)
def integration_pair(hs,hp,p):
 m=hs.t<=30;f,a=plt.subplots(figsize=(9,5));a.plot(hs.t[m],hs.tg[m],'k-',label='Gaz HC');a.plot(hs.t[m],hs.ta[m],color='tab:red',label='Suspente secondaire');a.plot(hp.t[m],hp.ta[m],color='tab:purple',label='Suspension principale');a.set(xlabel='Temps (min)',ylabel='Température (°C)',title="Cas critique, intégration jusqu'à 30 min");a.grid();a.legend();return save(f,p)
