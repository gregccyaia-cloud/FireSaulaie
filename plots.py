import numpy as np, matplotlib.pyplot as plt
COLOR={'HC':'tab:green','ISO 834':'tab:blue','Feu extérieur':'tab:orange'}
STYLE={'HC':'-','ISO 834':'--','Feu extérieur':'-.'}
def save(f,p):f.tight_layout();f.savefig(p,dpi=200,bbox_inches='tight');plt.close(f)
def fireplot(tm,curves,p):
 f,a=plt.subplots(figsize=(8.5,4.7))
 for name,y in curves.items():a.plot(tm,y,color=COLOR[name],ls='-',lw=2.2,label=name)
 a.set(title='Courbes nominales température-temps',xlabel='Temps (min)',ylabel='Température des gaz (°C)');a.grid(alpha=.3);a.legend();save(f,p)
def geom(pos,p):
 f,a=plt.subplots(figsize=(8.5,4.5));x=range(3)
 for key,lab,col in [('deck','Intrados','tab:blue'),('hanger','Naissance suspente','tab:orange'),('cable','Axe câble','tab:green')]:a.plot(x,[q[key] for q in pos],'-o',color=col,lw=2,label=lab)
 a.set_xticks(x,[q['code'] for q in pos]);a.set(title='Trois coupes géométriques de référence et positions F1, F2 et F3',ylabel='Hauteur (m)');a.grid(alpha=.3);a.legend();save(f,p)
def family(cases,el,L,p,title):
 f,a=plt.subplots(figsize=(8.7,4.8))
 for c in cases:
  if c['L']==L:a.plot(c['tm'],c[el],color=COLOR[c['fire']],ls=STYLE[c['fire']],lw=1.8,alpha=.85,label=c['fire']+' - '+c['pos'])
 h,l=a.get_legend_handles_labels();by=dict(zip(l,h));a.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');a.grid(alpha=.3);a.legend(by.values(),by.keys(),ncol=3,fontsize=7);save(f,p)
def ratio_plot(rows,el,p,title):
 f,a=plt.subplots(figsize=(8.7,4.8))
 for fire in COLOR:
  s=rows[(rows.Organe==el)&(rows.Feu==fire)];a.plot(s['t (min)'],s['ηfi'],color=COLOR[fire],ls=STYLE[fire],marker='o',lw=2,label=fire)
 a.axhline(1,color='black',lw=1.5,label='Limite ηfi = 1');a.set(title=title,xlabel='Temps (min)',ylabel='Ratio ηfi');a.grid(alpha=.3);a.legend();save(f,p)
def envelope(cases,fire,el,p,title):
 f,a=plt.subplots(figsize=(8.5,4.7));s=[c for c in cases if c['fire']==fire];Y=np.vstack([c[el] for c in s]);tm=s[0]['tm']
 for c in s:a.plot(tm,c[el],color=COLOR[fire],ls=STYLE[fire],lw=.8,alpha=.32,label=f"{c['pos']} - {c['L']:g} m")
 a.fill_between(tm,Y.min(0),Y.max(0),color=COLOR[fire],alpha=.15,label='Domaine min.-max.');a.plot(tm,Y.max(0),color=COLOR[fire],ls=STYLE[fire],lw=2.5,label='Enveloppe maximale');a.set(title=title,xlabel='Temps (min)',ylabel='Température acier (°C)');a.grid(alpha=.3);h,l=a.get_legend_handles_labels();by=dict(zip(l,h));a.legend(by.values(),by.keys(),ncol=3,fontsize=7);save(f,p)
