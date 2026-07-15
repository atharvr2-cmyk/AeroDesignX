"""
NACA 4-Digit Airfoil Generator

Generates NACA 4-digit airfoil geometry from the airfoil designation.
"""
import math
import numpy as np

class NACA4Airfoil:
    """
    Represents a NACA 4-digit airfoil.
    """

    def __init__(self, code, num_points=100):
        """
        Parameters
        ----------
        code : str
            Four-digit NACA designation (e.g. "4412")
        num_points : int
            Number of coordinate points
        """

        if len(code) != 4 or not code.isdigit():
            raise ValueError(
                "Airfoil code must be a 4-digit string."
            )

        self.code = code
        self.num_points = num_points

        # Decode the airfoil

        self.max_camber = int(code[0]) / 100
        self.camber_position = int(code[1]) / 10
        self.thickness = int(code[2:]) / 100

        if not isinstance(num_points, int) or num_points < 10:
            raise ValueError(
        "num_points must be an integer greater than or equal to 10."
    )
        
        if self.max_camber > 0 and self.camber_position == 0:
            raise ValueError(
        "A cambered NACA airfoil must have a nonzero "
        "camber-position digit."
    ) 

    def display_info(self):
        """
        Display the decoded airfoil parameters.
        """

        print("\n----- NACA Airfoil -----")
        print(f"Code:               {self.code}")
        print(f"Maximum Camber:     {self.max_camber:.2f}")
        print(f"Camber Position:    {self.camber_position:.2f}")
        print(f"Thickness Ratio:    {self.thickness:.2f}")
        print(f"Coordinate Points:  {self.num_points}")

    def thickness_distribution(self, x):
        """
        Calculate the half-thickness distribution.

        Parameters
        ----------
        x : float
            Chordwise location (0 to 1)

        Returns
        -------
        float
            Half thickness at x.
        """

        t = self.thickness

        return (
            5
            * t
            * (
                0.2969 * math.sqrt(x)
                - 0.1260 * x
                - 0.3516 * x**2
                + 0.2843 * x**3
                - 0.1015 * x**4
            )
        )
    
    def camber_line(self, x):
        """
        Calculate the camber line and its slope at a given x position.

        Returns
        -------
        yc : float
            Camber line height
        dyc_dx : float
            Camber line slope
        """

        m = self.max_camber
        p = self.camber_position

        if m == 0:
            return 0.0, 0.0

        if x < p:
            yc = (m / p**2) * (2 * p * x - x**2)
            dyc_dx = (2 * m / p**2) * (p - x)
        else:
            yc = (m / (1 - p)**2) * (
                (1 - 2 * p) + 2 * p * x - x**2
            )
            dyc_dx = (2 * m / (1 - p)**2) * (p - x)

        return yc, dyc_dx
    
    def generate_coordinates(self):
        """
        Generate upper and lower surface coordinates.
        """

        beta = np.linspace(0.0, math.pi, self.num_points)
        x_values = 0.5 * (1.0 - np.cos(beta))

        upper = []
        lower = []

        for x in x_values:

            yt = self.thickness_distribution(x)
            yc, dyc_dx = self.camber_line(x)

            theta = math.atan(dyc_dx)

            xu = x - yt * math.sin(theta)
            yu = yc + yt * math.cos(theta)

            xl = x + yt * math.sin(theta)
            yl = yc - yt * math.cos(theta)

            upper.append((xu, yu))
            lower.append((xl, yl))

        return upper, lower