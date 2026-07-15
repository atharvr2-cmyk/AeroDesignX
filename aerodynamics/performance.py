import math

"""
Performance Calculations

Functions related to aircraft performance.
"""


def dynamic_pressure(aircraft):
    """
    Calculate dynamic pressure.

    q = 0.5 * rho * V^2
    """

    return 0.5 * aircraft.air_density * aircraft.cruise_speed ** 2

"""
Aircraft Performance Calculations

Functions for calculating important aircraft performance metrics.
"""


def wing_loading(weight, wing_area):
    """
    Calculate aircraft wing loading.

    Parameters
    ----------
    weight : float
        Aircraft weight in newtons.

    wing_area : float
        Wing planform area in square meters.

    Returns
    -------
    float
        Wing loading in N/m^2.
    """

    return weight / wing_area


def stall_speed(
    weight,
    air_density,
    wing_area,
    cl_max,
):
    """
    Calculate aircraft stall speed.

    Parameters
    ----------
    weight : float
        Aircraft weight in newtons.

    air_density : float
        Air density in kg/m^3.

    wing_area : float
        Wing planform area in square meters.

    cl_max : float
        Maximum lift coefficient.

    Returns
    -------
    float
        Stall speed in m/s.
    """

    return math.sqrt(
        (2 * weight)
        / (air_density * wing_area * cl_max)
    )

def lift_to_drag_ratio(lift, drag):
    """
    Calculate aerodynamic lift-to-drag ratio.

    Parameters
    ----------
    lift : float
        Lift force in newtons.

    drag : float
        Drag force in newtons.

    Returns
    -------
    float
        Lift-to-drag ratio.
    """

    if drag <= 0:
        raise ValueError("Drag must be greater than zero.")

    return lift / drag


def stall_speed_margin(cruise_speed, stall_speed_value):
    """
    Calculate cruise speed as a multiple of stall speed.
    """

    if stall_speed_value <= 0:
        raise ValueError("Stall speed must be greater than zero.")

    return cruise_speed / stall_speed_value