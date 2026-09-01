from pathlib import Path
import matplotlib.pyplot as plt

def _finish(fig, path, show=False):
    fig.tight_layout(); fig.savefig(path,dpi=180,bbox_inches="tight")
    if show: plt.show()
    plt.close(fig)

def plot_fire_curves(time_min, scenarios, out_path, show=False):
    fig,ax=plt.subplots(figsize=(8,5))
    for s in scenarios: ax.plot(time_min,s.gas_temperature_c(time_min),label=s.label)
    ax.set(xlabel="Temps (min)",ylabel="Temperature des gaz (degC)",title="Courbes nominales de feu")
    ax.grid(True,alpha=.3); ax.legend(); _finish(fig,out_path,show)

def plot_case(df, title, out_path, show=False):
    fig,ax=plt.subplots(figsize=(8,5))
    for c,label in [("T_gas_C","Gaz"),("T_deck_C","Intrados"),("T_hanger_C","Suspente"),("T_cable_C","Cable principal")]: ax.plot(df["time_min"],df[c],label=label)
    ax.set(xlabel="Temps (min)",ylabel="Temperature (degC)",title=title)
    ax.grid(True,alpha=.3); ax.legend(); _finish(fig,out_path,show)

def plot_envelope(df, out_path, show=False):
    fig,ax=plt.subplots(figsize=(8,5))
    for c,label in [("T_deck_C","Intrados"),("T_hanger_C","Suspente"),("T_cable_C","Cable principal")]: ax.plot(df["time_min"],df[c],label=label)
    ax.set(xlabel="Temps (min)",ylabel="Temperature enveloppe (degC)",title="Enveloppe de tous les cas V1.1")
    ax.grid(True,alpha=.3); ax.legend(); _finish(fig,out_path,show)
