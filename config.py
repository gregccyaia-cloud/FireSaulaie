from dataclasses import dataclass

# ------------------------------------------------------------------
# REFERENCES
#
# ISO 834 :
# EN 1991-1-2 §3.2.1
#
# Feu extérieur :
# EN 1991-1-2 §3.2.2
#
# Ponts routiers :
# Guide CEREMA
# "Résistance à l'incendie des ponts routiers"
# ------------------------------------------------------------------

T_MAX_MIN = 120
DT_SECONDS = 5

READ_TIMES = [15, 30, 60, 90, 120]

VERBOSE = True

# ------------------------------------------------------------------
# M7
# ------------------------------------------------------------------

M7_WIDTH = 27.0

# Position du foyer (bord ouest = 0 m)

F1_X = 4.5
F2_X = 13.5
F3_X = 22.5

# ------------------------------------------------------------------
# Géométrie
# ------------------------------------------------------------------

DECK_WIDTH = 7.40

MAIN_CABLE_DIAMETER = 0.132
HANGER_DIAMETER = 0.042

HANGER_SPACING = 6.25

# Longueurs de foyers étudiées

FIRE_LENGTHS = [10.0, 15.0, 20.0]

# ------------------------------------------------------------------
# Matériau acier
# ------------------------------------------------------------------

STEEL_DENSITY = 7850.0

# valeur moyenne suffisante pour V1
STEEL_CP = 600.0

STEEL_EMISSIVITY = 0.7

AMBIENT_TEMP = 20.0