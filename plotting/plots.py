import matplotlib.pyplot as plt
def finish(fig,path,show=False): fig.tight_layout();fig.savefig(path,dpi=180,bbox_inches='tight');plt.show() if show else None;plt.close(fig)
def fire_curves(t,scenarios,path):
 fig,ax=plt.subplots(figsize=(8.2,4.8));[ax.plot(t,s.temperature(t),label=s.label,lw=2) for s in scenarios];ax.set(title='Courbes nominales de feu',xlabel='Temps (min)',ylabel='Temperature des gaz (degC)');ax.grid(alpha=.3);ax.legend();finish(fig,path)
def case(df,title,path):
 fig,ax=plt.subplots(figsize=(8.2,4.8))
 for c,l in [('T_gas_C','Gaz'),('T_deck_C','Intrados'),('T_hanger_C','Suspente'),('T_cable_C','Cable principal')]:ax.plot(df.time_min,df[c],label=l)
 ax.set(title=title,xlabel='Temps (min)',ylabel='Temperature (degC)');ax.grid(alpha=.3);ax.legend();finish(fig,path)
def geometry_profile(xs,deck,cable,path):
 fig,ax=plt.subplots(figsize=(8.2,4.3));ax.plot(xs,deck,label='Intrados minimal',lw=2);ax.plot(xs,cable,label='Axe cable principal',lw=2);ax.fill_between(xs,0,deck,alpha=.08);ax.set(title='Geometrie longitudinale simplifiee',xlabel='Abscisse ouest-est (m)',ylabel='Hauteur sur chaussee (m)');ax.grid(alpha=.3);ax.legend();finish(fig,path)
def convergence(t,a,b,path):
 fig,ax=plt.subplots(figsize=(8.2,4.3));ax.plot(t,a,label='Pas 5 s');ax.plot(t,b,label='Pas 2,5 s',ls='--');ax.set(title='Controle de convergence temporelle',xlabel='Temps (min)',ylabel='Temperature suspente (degC)');ax.grid(alpha=.3);ax.legend();finish(fig,path)
