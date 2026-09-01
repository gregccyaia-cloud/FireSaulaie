import numpy as np
import matplotlib.pyplot as plt
COL={'F1':'tab:blue','F2':'tab:orange','F3':'tab:green'}
def save(fig,p):fig.tight_layout();fig.savefig(p,dpi=190,bbox_inches='tight');plt.close(fig)
def fire_curves(t,sc,p):
 fig,ax=plt.subplots(figsize=(8,4.4));[ax.plot(t,s.temperature(t),lw=2,label=s.label) for s in sc];ax.set(title='Courbes nominales température-temps',xlabel='Temps (min)',ylabel='Température des gaz (°C)');ax.grid(alpha=.3);ax.legend();save(fig,p)
def geometry(pos,p):
 fig,ax=plt.subplots(figsize=(8,4.3));x=[q.x for q in pos];ax.plot(x,[q.h_deck for q in pos],'o-',label='Point bas de l’intrados');ax.plot(x,[q.h_hanger for q in pos],'o-',label='Naissance des suspentes');ax.plot(x,[q.h_cable for q in pos],'o-',label='Axe du câble principal');ax.set_xticks(x,[q.code for q in pos]);ax.set(title='Trois coupes géométriques de référence et positions F1, F2 et F3',xlabel='Position de feu',ylabel='Hauteur au-dessus de la chaussée (m)');ax.grid(alpha=.3);ax.legend();save(fig,p)
def family(cases,element,L,p,title):
 fig,ax=plt.subplots(figsize=(8.5,4.7));col='T_'+element
 for c in cases:
  if c['L']!=L:continue
  ls='--' if c['fire']=='ISO834' else '-';ax.plot(c['df'].time_min,c['df'][col],color=COL[c['pos']],ls=ls,lw=2,label=('ISO 834' if c['fire']=='ISO834' else 'Feu extérieur')+' - '+c['pos'])
 ax.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');ax.grid(alpha=.3);ax.legend(ncol=2,fontsize=8);save(fig,p)
def envelope(cases,fire,element,p,title):
 fig,ax=plt.subplots(figsize=(8.5,4.7));arr=[];time=None
 for c in cases:
  if c['fire']!=fire:continue
  y=c['df']['T_'+element].to_numpy();time=c['df'].time_min.to_numpy();arr.append(y);ax.plot(time,y,color=COL[c['pos']],ls='--' if fire=='ISO834' else '-',lw=.9,alpha=.55,label=f"{c['pos']} - L={c['L']:g} m")
 Y=np.vstack(arr);lo=Y.min(0);hi=Y.max(0);ax.fill_between(time,lo,hi,color='0.75',alpha=.5,label='Domaine min.-max.');ax.plot(time,hi,color='black',lw=2.3,label='Enveloppe maximale');ax.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');ax.grid(alpha=.3);ax.legend(ncol=3,fontsize=7);save(fig,p)
def integration(df,p):
 fig,ax=plt.subplots(figsize=(8,4.2));ax.plot(df.time_min,df.T_hanger,lw=2);ax.axvline(30,color='r',ls='--',label='30 min');ax.set(title='Processus d’intégration temporelle du cas critique',xlabel='Temps (min)',ylabel='Température acier (°C)');ax.grid(alpha=.3);ax.legend();save(fig,p)
