from pathlib import Path
import matplotlib.pyplot as plt
LINE_STYLES={("F1",10.):'-',("F1",15.):'--',("F1",20.):':',("F2",10.):'-',("F2",15.):'--',("F2",20.):':',("F3",10.):'-',("F3",15.):'--',("F3",20.):':'}
COLORS={'F1':'tab:blue','F2':'tab:orange','F3':'tab:green'}
def save(fig,path):
    path=Path(path); fig.tight_layout(); fig.savefig(path,dpi=200,bbox_inches='tight'); plt.close(fig); return path
def fire_plot(t,curves,path):
    f,a=plt.subplots(figsize=(9,5.2))
    for k,v in curves.items(): a.plot(t,v,lw=2,label=k)
    a.set(xlabel='Temps (min)',ylabel='Température des gaz (°C)',title='Courbes nominales température-temps'); a.grid(); a.legend(); return save(f,path)
def steel_plot(t,series,title,path,note_overlap=False):
    f,a=plt.subplots(figsize=(9,5.2))
    for label,values,code,L in series:
        a.plot(t,values,lw=1.65,label=label,color=COLORS[code],linestyle=LINE_STYLES[(code,L)],alpha=.90)
    a.set(xlabel='Temps (min)',ylabel="Température de l'acier (°C)",title=title); a.grid(); a.legend(fontsize=7,ncol=2)
    if note_overlap:a.text(.02,.03,"Les courbes se superposent dans la V1.4 car Φ = 1,0 et l'exposition est uniforme.",transform=a.transAxes,fontsize=8,bbox=dict(facecolor='white',alpha=.8,edgecolor='0.7'))
    return save(f,path)
def geometry_plot(sections,path):
    f,a=plt.subplots(figsize=(9,5.2)); x=range(3)
    a.plot(x,[s.intrados_m for s in sections],'o-',label="Point bas de l'intrados")
    a.plot(x,[s.intrados_m+.82 for s in sections],'o-',label='Naissance des suspentes')
    a.plot(x,[s.cable_m for s in sections],'o-',label='Axe du câble principal')
    a.set_xticks(list(x),[s.code for s in sections]); a.set(ylabel='Hauteur au-dessus de la chaussée (m)',title='Trois coupes géométriques de référence'); a.grid(); a.legend(); return save(f,path)
