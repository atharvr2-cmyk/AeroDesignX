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