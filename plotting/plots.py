import matplotlib.pyplot as plt
from data.config import SHOW_PLOTS
def save(fig,path):fig.tight_layout();fig.savefig(path,dpi=180,bbox_inches='tight');plt.show() if SHOW_PLOTS else None;plt.close(fig)
def fire_plot(t,sc,path):
 fig,ax=plt.subplots(figsize=(8,4.5));[ax.plot(t,s.temperature(t),lw=2,label=s.label) for s in sc];ax.set(title='Courbes nominales de feu',xlabel='Temps (min)',ylabel='Température (°C)');ax.grid(alpha=.3);ax.legend();save(fig,path)
def case_plot(df,title,path):
 fig,ax=plt.subplots(figsize=(8,4.5))
 for c,l in [('T_gas','Gaz'),('T_deck','Intrados'),('T_hanger','Suspente'),('T_cable','Câble principal')]:ax.plot(df.time_min,df[c],label=l)
 ax.set(title=title,xlabel='Temps (min)',ylabel='Température (°C)');ax.grid(alpha=.3);ax.legend();save(fig,path)
def equation_plot(path):
 fig,ax=plt.subplots(figsize=(10,2.5));ax.axis('off')
 ax.text(.02,.68,r'$\theta_{g,ISO}(t)=20+345\log_{10}(8t+1)$',fontsize=18)
 ax.text(.02,.22,r'$\theta_{g,ext}(t)=660\left(1-0.687e^{-0.32t}-0.313e^{-3.8t}\right)+20$',fontsize=18)
 save(fig,path)
