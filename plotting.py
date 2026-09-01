from pathlib import Path
import matplotlib.pyplot as plt
COL={'F1':'tab:blue','F2':'tab:orange','F3':'tab:green'};LS={10.:'-',15.:'--',20.:':'}
def save(fig,path):path=Path(path);fig.tight_layout();fig.savefig(path,dpi=200,bbox_inches='tight');plt.close(fig);return path
def fire_plot(t,curves,path):
 f,a=plt.subplots(figsize=(9,5.2));[a.plot(t,v,lw=2,label=k) for k,v in curves.items()];a.set(xlabel='Temps (min)',ylabel='Température des gaz (°C)',title='Courbes nominales température-temps');a.grid();a.legend();return save(f,path)
def steel_plot(t,series,title,path):
 f,a=plt.subplots(figsize=(9,5.2))
 for label,v,code,L in series:a.plot(t,v,lw=1.6,label=label,color=COL[code],linestyle=LS[L],alpha=.9)
 a.set(xlabel='Temps (min)',ylabel="Température de l'acier (°C)",title=title);a.grid();a.legend(fontsize=7,ncol=2);a.text(.02,.03,"Superpositions dues à Φ = 1,0 et à l'exposition uniforme.",transform=a.transAxes,fontsize=8,bbox=dict(facecolor='white',alpha=.85,edgecolor='.7'));return save(f,path)
def geometry_plot(sections,path):
 f,a=plt.subplots(figsize=(9,5.2));x=range(3);a.plot(x,[s.intrados_m for s in sections],'o-',label="Intrados");a.plot(x,[s.intrados_m+.82 for s in sections],'o-',label='Naissance suspente');a.plot(x,[s.cable_m for s in sections],'o-',label='Axe câble');a.set_xticks(list(x),[s.code for s in sections]);a.set(ylabel='Hauteur au-dessus de la chaussée (m)',title='Trois coupes géométriques de référence');a.grid();a.legend();return save(f,path)

def integration_plot(history, time_limit_min, path):
    """Visualise l'intégration depuis t=0 jusqu'à l'instant détaillé."""
    mask=history.t<=time_limit_min+1e-9
    f,a=plt.subplots(figsize=(9,5.2))
    a.plot(history.t[mask],history.tg[mask],lw=2,label='Température des gaz θg')
    a.plot(history.t[mask],history.ta[mask],lw=2,label="Température de l'acier θa")
    a.set(xlabel='Temps (min)',ylabel='Température (°C)',title=f'Intégration temporelle jusqu’à {time_limit_min:g} min')
    a.grid();a.legend()
    return save(f,path)
