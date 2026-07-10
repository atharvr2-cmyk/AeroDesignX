"""
Aircraft Assembly

Defines the Aircraft class that stores the
overall aircraft properties.
"""

from config.parameters import *
from geometry.wing import Wing

class Aircraft:
    def __init__(self):
        # General information
        self.name = AIRCRAFT_NAME

        # Physical properties
        self.mass = MASS
        self.gravity = GRAVITY

        # Wing properties
        self.wing_span = WING_SPAN
        self.wing_area = WING_AREA
        self.wing_chord = WING_CHORD
        self.airfoil = AIRFOIL

        self.wing = Wing(
            self.wing_span,
            self.wing_area,
            self.wing_chord,
            self.airfoil
        )

        # Flight conditions
        self.cruise_speed = CRUISE_SPEED
        self.air_density = AIR_DENSITY

    def display_info(self):
        """Print a summary of the aircraft."""

        print("\n========== Aircraft Summary ==========")
        print(f"Name:           {self.name}")
        print(f"Mass:           {self.mass:.2f} kg")
        print(f"Wing Span:      {self.wing_span:.2f} m")
        print(f"Wing Area:      {self.wing_area:.3f} m²")
        print(f"Wing Chord:     {self.wing_chord:.3f} m")
        print(f"Cruise Speed:   {self.cruise_speed:.2f} m/s")
        print(f"Airfoil:        {self.airfoil}")
        print("======================================")

        self.wing.display_info()