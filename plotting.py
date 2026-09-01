from pathlib import Path
import matplotlib.pyplot as plt
def save(fig,path):
    path=Path(path); fig.tight_layout(); fig.savefig(path,dpi=200,bbox_inches='tight'); plt.close(fig); return path
def fire_plot(t,curves,path):
    f,a=plt.subplots(figsize=(9,5.2))
    for k,v in curves.items(): a.plot(t,v,lw=2,label=k)
    a.set(xlabel='Temps (min)',ylabel='Température des gaz (°C)',title='Courbes nominales température-temps'); a.grid(); a.legend(); return save(f,path)
def steel_plot(t,series,title,path):
    f,a=plt.subplots(figsize=(9,5.2))
    for k,v in series.items(): a.plot(t,v,lw=1.8,label=k)
    a.set(xlabel='Temps (min)',ylabel="Température de l'acier (°C)",title=title); a.grid(); a.legend(fontsize=8); return save(f,path)
def geometry_plot(sections,path):
    f,a=plt.subplots(figsize=(9,5.2)); x=range(3)
    a.plot(x,[s.intrados_m for s in sections],'o-',label="Point bas de l'intrados")
    a.plot(x,[s.intrados_m+.82 for s in sections],'o-',label='Naissance des suspentes')
    a.plot(x,[s.cable_m for s in sections],'o-',label='Axe du câble principal')
    a.set_xticks(list(x),[s.code for s in sections]); a.set(ylabel='Hauteur au-dessus de la chaussée (m)',title='Trois coupes géométriques de référence'); a.grid(); a.legend(); return save(f,path)
