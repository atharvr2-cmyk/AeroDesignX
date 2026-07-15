"""
Drag Calculations

Functions for calculating aerodynamic drag coefficients
and drag force.
"""

import math


def induced_drag_coefficient(cl, aspect_ratio, oswald_efficiency=0.8):
    """
    Calculate the induced drag coefficient.

    Parameters
    ----------
    cl : float
        Lift coefficient.

    aspect_ratio : float
        Wing aspect ratio.

    oswald_efficiency : float
        Oswald efficiency factor.

    Returns
    -------
    float
        Induced drag coefficient.
    """

    return cl**2 / (
        math.pi * oswald_efficiency * aspect_ratio
    )


def total_drag_coefficient(
    cl,
    aspect_ratio,
    cd0=0.03,
    oswald_efficiency=0.8,
):
    """
    Calculate total drag coefficient using a parabolic drag polar.
    """

    induced_cd = induced_drag_coefficient(
        cl=cl,
        aspect_ratio=aspect_ratio,
        oswald_efficiency=oswald_efficiency,
    )

    return cd0 + induced_cd


def drag_force(
    air_density,
    velocity,
    wing_area,
    cd,
):
    """
    Calculate aerodynamic drag force in newtons.
    """

    dynamic_pressure = 0.5 * air_density * velocity**2

    return dynamic_pressure * wing_area * cd