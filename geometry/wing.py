"""
Wing Geometry

Defines the wing component of the aircraft.

This module stores the wing geometry and computes important
aerodynamic properties such as:
- Wing Area
- Aspect Ratio
- Taper Ratio
- Mean Aerodynamic Chord (MAC)
"""

import math


class Wing:
    """
    Represents a tapered aircraft wing.
    """

    def __init__(
        self,
        span,
        root_chord,
        tip_chord,
        airfoil,
        dihedral=0,
        sweep=0,
    ):
        """
        Initialize the wing geometry.

        Parameters
        ----------
        span : float
            Wingspan (m)
        root_chord : float
            Root chord length (m)
        tip_chord : float
            Tip chord length (m)
        airfoil : str
            Airfoil designation
        dihedral : float
            Dihedral angle (degrees)
        sweep : float
            Sweep angle (degrees)
        """

        self.span = span
        self.root_chord = root_chord
        self.tip_chord = tip_chord
        self.airfoil = airfoil

        self.dihedral = dihedral
        self.sweep = sweep

        # Calculated properties
        self.area = self.calculate_area()
        self.taper_ratio = self.tip_chord / self.root_chord

    def calculate_area(self):
        """
        Calculate the trapezoidal wing planform area.
        """
        return (
            (self.root_chord + self.tip_chord)
            * self.span
            / 2
        )

    def aspect_ratio(self):
        """
        Return the wing aspect ratio.
        """
        return self.span ** 2 / self.area

    def mean_aerodynamic_chord(self):
        """
        Calculate the Mean Aerodynamic Chord (MAC).
        """
        taper = self.taper_ratio

        return (
            (2 / 3)
            * self.root_chord
            * ((1 + taper + taper**2) / (1 + taper))
        )
    
    def wing_outline(self):
        """
        Returns the four corner points of the wing
        planform.

        Coordinate System:
        x = chordwise direction
        y = spanwise direction
        z = vertical direction
        """

        half_span = self.span / 2

        root_le = (0.0, 0.0, 0.0)
        root_te = (self.root_chord, 0.0, 0.0)

        tip_le = (0.0, half_span, 0.0)
        tip_te = (self.tip_chord, half_span, 0.0)

        return {
            "Root Leading Edge": root_le,
            "Root Trailing Edge": root_te,
            "Tip Leading Edge": tip_le,
            "Tip Trailing Edge": tip_te,
        }

    def display_info(self):
        """
        Display the wing geometry and calculated properties.
        """

        print("\n----- Wing Geometry -----")
        print(f"Span:               {self.span:.2f} m")
        print(f"Root Chord:         {self.root_chord:.3f} m")
        print(f"Tip Chord:          {self.tip_chord:.3f} m")
        print(f"Area:               {self.area:.3f} m²")
        print(f"Taper Ratio:        {self.taper_ratio:.3f}")
        print(f"Aspect Ratio:       {self.aspect_ratio():.2f}")
        print(f"Mean Aero Chord:    {self.mean_aerodynamic_chord():.3f} m")
        print(f"Dihedral:           {self.dihedral:.1f}°")
        print(f"Sweep:              {self.sweep:.1f}°")
        print(f"Airfoil:            {self.airfoil}")
        
        print("\nWing Outline Coordinates")

        for name, point in self.wing_outline().items():
            print(f"{name:<22}: {point}")