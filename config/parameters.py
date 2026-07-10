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
# Wing Parameters
# -------------------------

WING_SPAN = 1.0             # meters
WING_AREA = 0.25            # square meters
WING_CHORD = 0.25           # meters

AIRFOIL = "NACA4412"


# -------------------------
# Flight Conditions
# -------------------------

CRUISE_SPEED = 4.47         # m/s (~10 mph)
AIR_DENSITY = 1.225         # kg/m^3 at sea level


# -------------------------
# Design Constraints
# -------------------------

MAX_WING_LOADING = 150      # N/m^2