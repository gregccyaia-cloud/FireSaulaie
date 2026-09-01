# ------------------------------------------------------------------
# Profil intrados simplifié
#
# demi coupe :
#
# y = 0.00 m -> dz = 0.00 m
#
# y = 1.91 m -> dz = 0.19 m
#
# y = 3.70 m -> dz = 0.61 m
# ------------------------------------------------------------------


def intrados_rise(y):

    y = abs(y)

    if y <= 1.91:

        return (0.19 / 1.91) * y

    if y <= 3.70:

        return 0.19 + (0.42 / 1.79) * (y - 1.91)

    return 0.61


def hanger_section_factor():

    return 4.0 / 0.042


def cable_section_factor():

    return 4.0 / 0.132