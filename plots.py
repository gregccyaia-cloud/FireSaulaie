import numpy as np,matplotlib.pyplot as plt
COLOR={'HC':'tab:green','ISO 834':'tab:blue','Feu extérieur':'tab:orange'}
POS_LABEL={'F1':'OUEST','F2':'AXE M7','F3':'EST'}
POS_STYLE={'F1':'--','F2':'-','F3':'-.'}
def save(f,p):f.tight_layout();f.savefig(p,dpi=200,bbox_inches='tight');plt.close(f)
def fires(tm,curves,p):
 f,a=plt.subplots(figsize=(8.6,4.7))
 for n,y in curves.items():a.plot(tm,y,color=COLOR[n],lw=2.2,label=n)
 a.set(title='Courbes nominales température-temps',xlabel='Temps (min)',ylabel='Température des gaz (°C)');a.grid(alpha=.3);a.legend();save(f,p)
def geometry(pos,p):
 f,a=plt.subplots(figsize=(8.6,4.5));x=range(3)
 for k,l,c in [('deck','Intrados','tab:blue'),('hanger','Naissance suspente','tab:orange'),('cable','Axe câble','tab:green')]:a.plot(x,[q[k] for q in pos],'-o',color=c,lw=2,label=l)
 a.set_xticks(x,[POS_LABEL[q['code']] for q in pos]);a.set(title='Trois coupes géométriques de référence',ylabel='Hauteur (m)');a.grid(alpha=.3);a.legend();save(f,p)
def family(cases,el,H,p,title):
 f,a=plt.subplots(figsize=(8.7,4.8))
 for c in cases:
  if c['H']==H:a.plot(c['tm'],c[el],color=COLOR[c['fire']],ls=POS_STYLE[c['pos']],lw=1.8,alpha=.9,label=c['fire']+' - '+POS_LABEL[c['pos']])
 h,l=a.get_legend_handles_labels();by=dict(zip(l,h));a.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');a.grid(alpha=.3);a.legend(by.values(),by.keys(),ncol=3,fontsize=7);save(f,p)
def ratio(df,el,p,title):
 f,a=plt.subplots(figsize=(8.7,4.8))
 for fire in COLOR:
  for pos in ('F1','F2','F3'):
   s=df[(df.Organe==el)&(df.Feu==fire)&(df.Position==POS_LABEL[pos])];a.plot(s['Temps (min)'],s['ηfi'],color=COLOR[fire],ls=POS_STYLE[pos],marker='o',lw=1.7,label=fire+' - '+POS_LABEL[pos])
 a.axhline(1,color='black',lw=1.5,label='Limite ηfi = 1');a.set(title=title,xlabel='Temps (min)',ylabel='Ratio ηfi');a.grid(alpha=.3);h,l=a.get_legend_handles_labels();by=dict(zip(l,h));a.legend(by.values(),by.keys(),ncol=3,fontsize=7);save(f,p)
def envelope(cases,fire,el,p,title):
 f,a=plt.subplots(figsize=(8.6,4.8));s=[c for c in cases if c['fire']==fire];Y=np.vstack([c[el] for c in s]);tm=s[0]['tm']
 for c in s:a.plot(tm,c[el],color=COLOR[fire],ls=POS_STYLE[c['pos']],lw=.85,alpha=.38,label=f"{POS_LABEL[c['pos']]} - H={c['H']:g} m")
 a.fill_between(tm,Y.min(0),Y.max(0),color=COLOR[fire],alpha=.15,label='Domaine min.-max.');a.plot(tm,Y.max(0),color=COLOR[fire],lw=2.6,label='Enveloppe maximale');a.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');a.grid(alpha=.3);h,l=a.get_legend_handles_labels();by=dict(zip(l,h));a.legend(by.values(),by.keys(),ncol=3,fontsize=7);save(f,p)
def integration(c,p):
 f,a=plt.subplots(figsize=(8.5,4.5));a.plot(c['tm'],c['gas'],color=COLOR[c['fire']],label='Gaz '+c['fire']);a.plot(c['tm'],c['hanger'],color='black',label='Suspente secondaire');a.axvline(30,color='red',ls='--');a.set(title='Intégration temporelle du cas critique',xlabel='Temps (min)',ylabel='Température (°C)');a.grid(alpha=.3);a.legend();save(f,p)
