import matplotlib.pyplot as plt
def case_plot(df,title,path,show=False):
 fig,ax=plt.subplots(figsize=(8,5))
 for c,l in [('T_gas','Gaz'),('T_deck','Intrados'),('T_hanger','Suspente'),('T_cable','Cable')]:ax.plot(df.time_min,df[c],label=l)
 ax.set(title=title,xlabel='Temps (min)',ylabel='Temperature (degC)');ax.grid(alpha=.3);ax.legend();fig.tight_layout();fig.savefig(path,dpi=160)
 if show:plt.show()
 plt.close(fig)
def fire_plot(t,scenarios,path):
 fig,ax=plt.subplots(figsize=(8,5))
 for s in scenarios:ax.plot(t,s.temperature(t),label=s.label)
 ax.set(xlabel='Temps (min)',ylabel='Temperature (degC)',title='Courbes de feu');ax.grid(alpha=.3);ax.legend();fig.tight_layout();fig.savefig(path,dpi=160);plt.close(fig)
