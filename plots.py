import numpy as np,matplotlib.pyplot as plt
COLOR={'HC':'tab:green','ISO 834':'tab:blue','Feu extérieur':'tab:orange'};POS={'F1':'OUEST','F2':'AXE M7','F3':'EST'};STYLE={'F1':'--','F2':'-','F3':'-.'}
def sv(f,p):f.tight_layout();f.savefig(p,dpi=200,bbox_inches='tight');plt.close(f)
def fires(t,C,p):
 f,a=plt.subplots(figsize=(8.6,4.7));[a.plot(t,y,color=COLOR[n],lw=2.2,label=n) for n,y in C.items()];a.set(title='Courbes nominales température-temps',xlabel='Temps (min)',ylabel='Température des gaz (°C)');a.grid(alpha=.3);a.legend();sv(f,p)
def family(cases,e,H,p,title):
 f,a=plt.subplots(figsize=(8.7,4.8))
 for c in cases:
  if c['H']==H:a.plot(c['t'],c[e],color=COLOR[c['fire']],ls=STYLE[c['pos']],lw=1.8,label=c['fire']+' - '+POS[c['pos']])
 a.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');a.grid(alpha=.3);a.legend(ncol=3,fontsize=7);sv(f,p)
def ratios(df,e,p,title):
 f,a=plt.subplots(figsize=(8.7,4.8))
 for fire in COLOR:
  for pos in POS:
   s=df[(df.Organe==e)&(df.Feu==fire)&(df.Position==POS[pos])];a.plot(s['Temps'],s['ηfi'],color=COLOR[fire],ls=STYLE[pos],marker='o',lw=1.7,label=fire+' - '+POS[pos])
 a.axhline(1,color='black');a.set(title=title,xlabel='Temps (min)',ylabel='ηfi');a.grid(alpha=.3);a.legend(ncol=3,fontsize=7);sv(f,p)
def envelope(cases,fire,e,p,title):
 f,a=plt.subplots(figsize=(8.6,4.8));s=[c for c in cases if c['fire']==fire];Y=np.vstack([c[e] for c in s]);t=s[0]['t']
 for c in s:a.plot(t,c[e],color=COLOR[fire],ls=STYLE[c['pos']],lw=.8,alpha=.35,label=f"{POS[c['pos']]} - H={c['H']:g} m")
 a.fill_between(t,Y.min(0),Y.max(0),color=COLOR[fire],alpha=.15);a.plot(t,Y.max(0),color=COLOR[fire],lw=2.5,label='Enveloppe maximale');a.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');a.grid(alpha=.3);a.legend(ncol=3,fontsize=7);sv(f,p)
def integration(c,p):
 f,a=plt.subplots(figsize=(8.5,4.5));a.plot(c['t'],c['gas'],color=COLOR[c['fire']],label='Gaz');a.plot(c['t'],c['hanger'],color='black',label='Suspente');a.axvline(30,color='red',ls='--');a.set(title='Intégration temporelle du cas critique',xlabel='Temps (min)',ylabel='Température (°C)');a.grid(alpha=.3);a.legend();sv(f,p)
