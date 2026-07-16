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

def estimate_endurance(
    battery_capacity_wh,
    average_power_w,
    usable_fraction=0.8,
):
    """
    Estimate aircraft endurance.

    Parameters
    ----------
    battery_wh : float
        Battery energy capacity in watt-hours.

    power_w : float
        Average power consumption in watts.

    usable_fraction : float
        Fraction of battery capacity considered usable.
        Defaults to 0.8 to avoid completely draining the battery.

    Returns
    -------
    float
        Estimated endurance in hours.
    """

    if battery_capacity_wh <= 0:
        raise ValueError("Battery capacity must be greater than zero.")

    if average_power_w <= 0:
        raise ValueError("Power consumption must be greater than zero.")

    if not 0 < usable_fraction <= 1:
        raise ValueError("Usable fraction must be between 0 and 1.")

    usable_energy = battery_capacity_wh * usable_fraction

    return usable_energy / average_power_w


def estimate_range(cruise_speed, endurance_hours):
    """
    Estimate aircraft range.

    Parameters
    ----------
    cruise_speed : float
        Aircraft cruise speed in m/s.

    endurance_hours : float
        Aircraft endurance in hours.

    Returns
    -------
    float
        Estimated range in kilometers.
    """

    if cruise_speed <= 0:
        raise ValueError("Cruise speed must be greater than zero.")

    if endurance_hours <= 0:
        raise ValueError("Endurance must be greater than zero.")

    cruise_speed_kmh = cruise_speed * 3.6

    return cruise_speed_kmh * endurance_hours