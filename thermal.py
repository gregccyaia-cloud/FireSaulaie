import numpy as np

from config import (
    STEEL_DENSITY,
    STEEL_CP,
)

# ---------------------------------------------------------
# V1
#
# Approximation :
# température élément uniforme
#
# à améliorer ultérieurement
# ---------------------------------------------------------


def temperature_response(
        gas_temperature,
        section_factor,
        tau_seconds=800
):

    theta = np.zeros(len(gas_temperature))

    theta[0] = 20.

    for i in range(1, len(gas_temperature)):

        dt = 5

        dtheta = (
            (gas_temperature[i] - theta[i-1])
            * dt
            / tau_seconds
        )

        dtheta *= (
            section_factor / 30.0
        )

        theta[i] = theta[i-1] + dtheta

    return theta