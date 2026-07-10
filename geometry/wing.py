"""
Wing Geometry

Defines the wing component of the aircraft.
"""


class Wing:
    def __init__(self, span, area, chord, airfoil):
        self.span = span
        self.area = area
        self.chord = chord
        self.airfoil = airfoil

    def aspect_ratio(self):
        """Return the wing aspect ratio."""
        return self.span ** 2 / self.area

    def display_info(self):
        print("\n----- Wing Geometry -----")
        print(f"Span:          {self.span:.2f} m")
        print(f"Area:          {self.area:.3f} m²")
        print(f"Chord:         {self.chord:.3f} m")
        print(f"Airfoil:       {self.airfoil}")
        print(f"Aspect Ratio:  {self.aspect_ratio():.2f}")