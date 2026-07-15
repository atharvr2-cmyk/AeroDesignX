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
from airfoils.naca import NACA4Airfoil

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
        if span <= 0:
            raise ValueError("Wing span must be greater than zero.")

        if root_chord <= 0:
            raise ValueError("Root chord must be greater than zero.")

        if tip_chord <= 0:
            raise ValueError("Tip chord must be greater than zero.")

        if not isinstance(airfoil, str):
            raise TypeError("Airfoil designation must be a string.")

        self.span = span
        self.root_chord = root_chord
        self.tip_chord = tip_chord
        self.airfoil = airfoil

        self.dihedral = dihedral
        self.sweep = sweep

        # Calculated properties
        self.area = self.span * (self.root_chord + self.tip_chord) / 2
        self.taper_ratio = self.tip_chord / self.root_chord
    
    

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
        including sweep and dihedral.
        """

        half_span = self.span / 2

        sweep_offset = half_span * math.tan(math.radians(self.sweep))
        dihedral_offset = half_span * math.tan(math.radians(self.dihedral))

        root_le = (0.0, 0.0, 0.0)
        root_te = (self.root_chord, 0.0, 0.0)

        tip_le = (
            sweep_offset,
            half_span,
            dihedral_offset,
        )

        tip_te = (
            sweep_offset + self.tip_chord,
            half_span,
            dihedral_offset,
        )

        return {
            "Root Leading Edge": root_le,
            "Root Trailing Edge": root_te,
            "Tip Leading Edge": tip_le,
            "Tip Trailing Edge": tip_te,
        }


    def generate_sections(self, n_points=100):
        """
        Generate root and tip airfoil sections.
        """

        airfoil = NACA4Airfoil(
            self.airfoil,
            n_points
        )

        upper, lower = airfoil.generate_coordinates()

        # Combine upper and lower surfaces
        coordinates = upper + lower[::-1]

        root_section = []
        tip_section = []

        half_span = self.span / 2

        sweep_offset = half_span * math.tan(
            math.radians(self.sweep)
        )

        dihedral_offset = half_span * math.tan(
            math.radians(self.dihedral)
        )


        for x, z in coordinates:

            # Root airfoil
            root_section.append(
                (
                    x * self.root_chord,
                    0,
                    z * self.root_chord
                )
            )


            # Tip airfoil
            tip_section.append(
                (
                    sweep_offset + x * self.tip_chord,
                    half_span,
                    dihedral_offset + z * self.tip_chord
                )
            )


        return root_section, tip_section
    

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