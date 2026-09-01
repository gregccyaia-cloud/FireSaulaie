import matplotlib.pyplot as plt
from data.config import SHOW_PLOTS
def save(fig,path):fig.tight_layout();fig.savefig(path,dpi=200,bbox_inches='tight');plt.show() if SHOW_PLOTS else None;plt.close(fig)
def fire_plot(t,sc,path):
 fig,ax=plt.subplots(figsize=(8,4.5));[ax.plot(t,s.temperature(t),lw=2,label=s.label) for s in sc];ax.set(title='Courbes nominales de feu',xlabel='Temps (min)',ylabel='Température (°C)');ax.grid(alpha=.3);ax.legend();save(fig,path)
def equation_plot(path):
 fig,ax=plt.subplots(figsize=(10,2.7));ax.axis('off')
 ax.text(.02,.68,r'$\theta_{g,\mathrm{ISO}}(t)=20+345\,\log_{10}\!\left(8t+1\right)$',fontsize=19)
 ax.text(.02,.20,r'$\theta_{g,\mathrm{ext}}(t)=660\left(1-0{,}687e^{-0{,}32t}-0{,}313e^{-3{,}8t}\right)+20$',fontsize=19)
 save(fig,path)
def principles_plot(path):
 fig,ax=plt.subplots(figsize=(10,3.3));ax.axis('off')
 ax.text(.02,.78,r'$q_{\mathrm{conv}}=\alpha_{c}\left(\theta_g-\theta_a\right)$',fontsize=18)
 ax.text(.02,.46,r'$q_{\mathrm{rad}}=\Phi\,\varepsilon_m\varepsilon_f\sigma\left[\left(\theta_g+273{,}15\right)^4-\left(\theta_a+273{,}15\right)^4\right]$',fontsize=17)
 ax.text(.02,.12,r'$\dfrac{A_m}{V}=\eta_{\mathrm{exp}}\,\dfrac{4}{D}$',fontsize=18)
 save(fig,path)
def case_plot(df,title,path):
 fig,ax=plt.subplots(figsize=(8,4.5))
 for c,l in [('T_gas','Gaz'),('T_deck','Intrados'),('T_hanger','Suspente'),('T_cable','Câble principal')]:ax.plot(df.time_min,df[c],label=l)
 ax.set(title=title,xlabel='Temps (min)',ylabel='Température (°C)');ax.grid(alpha=.3);ax.legend();save(fig,path)
def family_plot(cases,element,hf,path,title):
 fig,ax=plt.subplots(figsize=(8.5,4.8))
 col=f'T_{element}'
 for stem,s,p,h,df,*_ in cases:
  if h==hf:ax.plot(df.time_min,df[col],label=f'{s.label} - {p.code}')
 ax.set(title=title,xlabel='Temps (min)',ylabel='Température (°C)');ax.grid(alpha=.3);ax.legend(ncol=2,fontsize=8);save(fig,path)
