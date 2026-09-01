from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
PNG_DIR = RESULTS_DIR / "png"
CSV_DIR = RESULTS_DIR / "csv"
REPORT_DIR = RESULTS_DIR / "reports"
LOG_DIR = ROOT / "logs"

SIM_DURATION_MIN = 120.0
TIME_STEP_SEC = 5.0
READ_TIMES_MIN = (15, 30, 60, 90, 120)
TEMPERATURE_THRESHOLDS_C = (400, 500, 600, 700)
VERBOSE = True
SAVE_PNG = True
SHOW_PLOTS = True
GENERATE_REPORT = True

INITIAL_TEMPERATURE_C = 20.0
STEEL_DENSITY_KG_M3 = 7850.0
STEEL_EMISSIVITY = 0.70
FIRE_EMISSIVITY = 1.00
CONVECTION_COEFF_W_M2K = 25.0
STEFAN_BOLTZMANN = 5.670374419e-8

# Screening geometry only. Not a normative flame model.
FLAME_MODEL = "vertical_column"
FLAME_HEIGHTS_M = (10.0, 12.0, 15.0)
TRUCK_LENGTH_M = 16.0
TRUCK_WIDTH_M = 2.5
TRUCK_HEIGHT_M = 4.0

# V1.1 exposure factors. Deliberately explicit and editable.
# 1.0 means direct exposure to the nominal gas temperature.
DECK_VIEW_FACTOR = 1.0
NEAR_HANGER_VIEW_FACTOR = 0.85
NEAR_CABLE_VIEW_FACTOR = 0.60
MASKED_HANGER_VIEW_FACTOR = 0.35
MASKED_CABLE_VIEW_FACTOR = 0.20

# PEHD option is prepared but disabled in V1.1.
MAIN_CABLE_PROTECTION = "none"  # "none" or "pehd_placeholder"
