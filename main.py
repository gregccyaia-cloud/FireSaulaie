import os
import numpy as np

from fire import (
    build_fire_curve
)

from geometry import (
    hanger_section_factor,
    cable_section_factor
)

from thermal import (
    temperature_response
)

from plotting import (
    save_curve
)

# -------------------------------------------------
# Création dossier résultats
# -------------------------------------------------

os.makedirs("results", exist_ok=True)

# -------------------------------------------------
# Temps
# -------------------------------------------------

times = np.arange(
    0,
    120.0 + 5.0/60.0,
    5.0/60.0
)

# -------------------------------------------------
# Courbes de feu
# -------------------------------------------------

iso_gas = build_fire_curve(
    "ISO",
    times
)

ext_gas = build_fire_curve(
    "EXTERNAL",
    times
)

save_curve(
    times,
    iso_gas,
    "ISO 834",
    "results/01_ISO834.png"
)

save_curve(
    times,
    ext_gas,
    "Feu Extérieur",
    "results/02_EXTERNAL.png"
)

# -------------------------------------------------
# Facteurs de section
# -------------------------------------------------

amv_hanger = hanger_section_factor()
amv_cable = cable_section_factor()

# -------------------------------------------------
# Suspente
# -------------------------------------------------

hanger_iso = temperature_response(
    iso_gas,
    amv_hanger
)

hanger_ext = temperature_response(
    ext_gas,
    amv_hanger
)

# -------------------------------------------------
# Câble principal
# -------------------------------------------------

cable_iso = temperature_response(
    iso_gas,
    amv_cable
)

cable_ext = temperature_response(
    ext_gas,
    amv_cable
)

save_curve(
    times,
    hanger_iso,
    "Suspente - ISO",
    "results/03_HANGER_ISO.png"
)

save_curve(
    times,
    cable_iso,
    "Câble principal - ISO",
    "results/04_CABLE_ISO.png"
)

# -------------------------------------------------
# Console
# -------------------------------------------------

print("="*60)
print("PASSERELLE GERLAND - LA SAULAIE")
print("ANALYSE INCENDIE - V1")
print("="*60)

print()

print(
    f"Suspente Tmax ISO : "
    f"{hanger_iso.max():.1f} °C"
)

print(
    f"Câble Tmax ISO : "
    f"{cable_iso.max():.1f} °C"
)

print()

print(
    f"Suspente Tmax Feu Extérieur : "
    f"{hanger_ext.max():.1f} °C"
)

print(
    f"Câble Tmax Feu Extérieur : "
    f"{cable_ext.max():.1f} °C"
)

print()

print("="*60)