from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
COL={'F1':'tab:blue','F2':'tab:orange','F3':'tab:green'};MARK={'F1':'o','F2':'s','F3':'^'}
def save(f,p):p=Path(p);f.tight_layout();f.savefig(p,dpi=210,bbox_inches='tight');plt.close(f);return p
def fire_style(name):return ':' if name.startswith('Feu 1') else '-'
def fire_plot(t,D,p):
 f,a=plt.subplots(figsize=(9,5));
 for k,v in D.items():a.plot(t,v,lw=2.2,linestyle=fire_style(k),label=k)
 a.set(xlabel='Temps (min)',ylabel='Température des gaz (°C)',title='Courbes nominales température-temps');a.grid();a.legend();return save(f,p)
def section_plot(t,series,title,ylabel,p):
 f,a=plt.subplots(figsize=(9,5))
 for fire,code,v in series:a.plot(t,v,color=COL[code],linestyle=fire_style(fire),lw=2,label=f'{fire} - {code}')
 a.set(xlabel='Temps (min)',ylabel=ylabel,title=title);a.grid();a.legend(fontsize=7,ncol=2);return save(f,p)
def envelope_plot(t,cases,title,ylabel,p):
 """Tous les cas, min/max et enveloppe; marqueurs décalés rendent visibles les coïncidences."""
 f,a=plt.subplots(figsize=(9,5.3));stack=np.vstack([v for _,_,_,v in cases]);lo=stack.min(0);hi=stack.max(0)
 for i,(fire,code,L,v) in enumerate(cases):
  ls=fire_style(fire);mark=MARK[code];a.plot(t,v,color=COL[code],linestyle=ls,lw=.9,alpha=.38,label=f'{fire} - {code} - L={int(L)} m',marker=mark,markevery=(20+i*7,220),markersize=3)
 a.fill_between(t,lo,hi,color='grey',alpha=.22,label='Faisceau min-max')
 a.plot(t,hi,color='black',lw=2.3,label='Enveloppe supérieure');a.plot(t,lo,color='black',lw=1.4,linestyle='--',label='Enveloppe inférieure')
 a.set(xlabel='Temps (min)',ylabel=ylabel,title=title);a.grid();a.legend(fontsize=6,ncol=3)
 if np.allclose(lo,hi):a.text(.02,.03,"Faisceau d'épaisseur nulle dans la V1.5_I : les cas coïncident avec Φ = 1,0.\nLes marqueurs décalés attestent la présence de toutes les séries.",transform=a.transAxes,fontsize=8,bbox=dict(facecolor='white',alpha=.9,edgecolor='.7'))
 return save(f,p)
def geom(S,p):
 f,a=plt.subplots(figsize=(9,5));x=range(3);a.plot(x,[s.intrados_m for s in S],'o-',label='Intrados');a.plot(x,[s.intrados_m+.82 for s in S],'o-',label='Naissance suspente');a.plot(x,[s.cable_m for s in S],'o-',label='Axe câble');a.set_xticks(list(x),[s.code for s in S]);a.set(ylabel='Hauteur (m)',title='Trois coupes géométriques');a.grid();a.legend();return save(f,p)
def integration_pair(hs,hp,p):
 m=hs.t<=30;f,a=plt.subplots(figsize=(9,5.2));a.plot(hs.t[m],hs.tg[m],color='black',lw=2,label='Gaz θg');a.plot(hs.t[m],hs.ta[m],color='tab:red',lw=2,label='Suspente secondaire');a.plot(hp.t[m],hp.ta[m],color='tab:purple',lw=2,label='Suspente principale - câble clos');a.set(xlabel='Temps (min)',ylabel='Température (°C)',title="Intégration comparée jusqu'à 30 min");a.grid();a.legend();return save(f,p)
