"""
Aircraft Assembly

Defines the Aircraft class that stores the
overall aircraft properties.
"""

from config.parameters import *
from geometry.wing import Wing


class Aircraft:
    def __init__(
        self,
        name=None,
        mass=None,
        gravity=None,
        cruise_speed=None,
        air_density=None,
        wing=None,
        airfoil=None
    ):
        """
        Create an aircraft.

        Parameters are optional so the class can still use the
        default values stored in config/parameters.py.

        A generated Wing object can also be supplied directly.
        """

        # General information
        self.name = name if name is not None else AIRCRAFT_NAME

        # Physical properties
        self.mass = mass if mass is not None else MASS
        self.gravity = gravity if gravity is not None else GRAVITY

        # Flight conditions
        self.cruise_speed = (
            cruise_speed
            if cruise_speed is not None
            else CRUISE_SPEED
        )

        self.air_density = (
            air_density
            if air_density is not None
            else AIR_DENSITY
        )

        # Airfoil
        self.airfoil = airfoil if airfoil is not None else AIRFOIL

        # Use a supplied wing or create the default wing.
        if wing is not None:
            self.wing = wing
        else:
            self.wing = Wing(
                WING_SPAN,
                WING_AREA,
                WING_CHORD,
                self.airfoil
            )

        # Keep aircraft-level wing properties synchronized
        # with the Wing object.
        self.wing_span = self.wing.span

        if hasattr(self.wing, "area"):
            if callable(self.wing.area):
                self.wing_area = self.wing.area()
            else:
                self.wing_area = self.wing.area
        else:
            self.wing_area = WING_AREA

        if hasattr(self.wing, "chord"):
            self.wing_chord = self.wing.chord
        elif hasattr(self.wing, "root_chord") and hasattr(
            self.wing,
            "tip_chord"
        ):
            self.wing_chord = (
                self.wing.root_chord + self.wing.tip_chord
            ) / 2
        else:
            self.wing_chord = WING_CHORD

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