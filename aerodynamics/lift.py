"""
Lift Calculations

Functions related to lift generation.
"""


def required_lift(mass, gravity):
    """
    Calculate the lift required for steady, level flight.

    In level flight, lift must equal aircraft weight.

    Parameters
    ----------
    mass : float
        Aircraft mass in kilograms.

    gravity : float
        Gravitational acceleration in m/s^2.

    Returns
    -------
    float
        Required lift in newtons.
    """

    return mass * gravity


def required_cl(
    mass,
    gravity,
    air_density,
    velocity,
    wing_area,
):
    """
    Calculate the lift coefficient required
    for steady, level flight.

    Parameters
    ----------
    mass : float
        Aircraft mass in kilograms.

    gravity : float
        Gravitational acceleration in m/s^2.

    air_density : float
        Air density in kg/m^3.

    velocity : float
        Flight speed in m/s.

    wing_area : float
        Wing area in m^2.

    Returns
    -------
    float
        Required lift coefficient.
    """

    lift = required_lift(mass, gravity)
    dynamic_pressure = 0.5 * air_density * velocity**2

    return lift / (dynamic_pressure * wing_area)