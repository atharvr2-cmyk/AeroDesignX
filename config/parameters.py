"""
AeroDesignX Aircraft Configuration Parameters

This file contains the main design inputs
for the aircraft generator.
"""

# -------------------------
# Aircraft General Properties
# -------------------------

AIRCRAFT_NAME = "AeroDesignX UAV"

MASS = 3.0                  # kg
GRAVITY = 9.81              # m/s^2

# -------------------------
# Flight Conditions
# -------------------------

CRUISE_SPEED = 15         # m/s (~10 mph)
AIR_DENSITY = 1.225         # kg/m^3 at sea level


# -------------------------
# Design Constraints
# -------------------------

MAX_WING_LOADING = 150      # N/m^2
CL_MAX = 1.4


# =========================
# Wing Parameters
# =========================

WING_SPAN = 1.20          # m
ROOT_CHORD = 0.36         # m
TIP_CHORD = 0.20          # m

DIHEDRAL = 5              # degrees
SWEEP = 0                 # degrees

AIRFOIL = "4412"

# Battery Parameters

BATTERY_CAPACITY_WH = 220.0      # Wh
AVERAGE_POWER_W = 180.0          # W
BATTERY_USABLE_FRACTION = 0.80   # 80% usable capacity

