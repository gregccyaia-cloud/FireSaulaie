from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class FireScenario:
    code: str
    label: str
    reference: str

    def gas_temperature_c(self, t_min):
        raise NotImplementedError

class ISO834(FireScenario):
    def __init__(self):
        super().__init__("ISO834", "Courbe ISO 834", "EN 1991-1-2, courbe nominale standard")

    def gas_temperature_c(self, t_min):
        t = np.asarray(t_min, dtype=float)
        return 20.0 + 345.0 * np.log10(8.0 * t + 1.0)

class CeremaExternal(FireScenario):
    def __init__(self):
        super().__init__("CEREMA_EXT", "Feu exterieur CEREMA", "Guide CEREMA 2018, formule fournie par le projet")

    def gas_temperature_c(self, t_min):
        t = np.asarray(t_min, dtype=float)
        return 660.0 * (1.0 - 0.687*np.exp(-0.32*t) - 0.313*np.exp(-3.8*t)) + 20.0

def default_fire_scenarios():
    return (ISO834(), CeremaExternal())
