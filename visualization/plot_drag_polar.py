"""
Drag Polar Visualization

Plots drag coefficient versus lift coefficient.
"""

import numpy as np
import matplotlib.pyplot as plt

from aerodynamics.drag import total_drag_coefficient


def plot_drag_polar(
    aspect_ratio,
    cd0=0.03,
    oswald_efficiency=0.8,
    operating_cl=None,
):
    """
    Plot the aircraft drag polar.

    Parameters
    ----------
    aspect_ratio : float
        Wing aspect ratio.

    cd0 : float
        Zero-lift drag coefficient.

    oswald_efficiency : float
        Oswald efficiency factor.

    operating_cl : float, optional
        Current operating lift coefficient.
    """

    cl_values = np.linspace(-0.5, 1.5, 200)

    cd_values = [
        total_drag_coefficient(
            cl=cl,
            aspect_ratio=aspect_ratio,
            cd0=cd0,
            oswald_efficiency=oswald_efficiency,
        )
        for cl in cl_values
    ]

    plt.figure(figsize=(8, 6))

    plt.plot(
        cd_values,
        cl_values,
        label="Drag Polar",
    )

    if operating_cl is not None:
        operating_cd = total_drag_coefficient(
            cl=operating_cl,
            aspect_ratio=aspect_ratio,
            cd0=cd0,
            oswald_efficiency=oswald_efficiency,
        )

        plt.scatter(
            operating_cd,
            operating_cl,
            s=70,
            label="Cruise Operating Point",
        )

    plt.title("Aircraft Drag Polar")
    plt.xlabel("Drag Coefficient, $C_D$")
    plt.ylabel("Lift Coefficient, $C_L$")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()