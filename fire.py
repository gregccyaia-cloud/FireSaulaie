import numpy as np

# ============================================================
# ISO 834
#
# EN 1991-1-2 §3.2.1
# ============================================================

def iso834_temperature(t_min):

    return 20.0 + 345.0 * np.log10(8.0 * t_min + 1.0)


# ============================================================
# FEU EXTERIEUR
#
# EN 1991-1-2 §3.2.2
# ============================================================

def external_fire_temperature(t_min):

    return (
        660.0
        * (
            1.0
            - 0.687 * np.exp(-0.32 * t_min)
            - 0.313 * np.exp(-3.8 * t_min)
        )
        + 20.0
    )


def build_fire_curve(curve_name, times):

    if curve_name == "ISO":
        return iso834_temperature(times)

    elif curve_name == "EXTERNAL":
        return external_fire_temperature(times)

    raise ValueError("Courbe inconnue")