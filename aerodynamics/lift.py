"""
Lift Calculations

Functions related to lift generation.
"""


def required_lift(aircraft):
    """
    Returns the lift required for level flight.
    """

    return aircraft.mass * aircraft.gravity

def required_cl(aircraft):
    """
    Calculate the lift coefficient required
    for steady level flight.
    """

    lift = required_lift(aircraft)

    q = 0.5 * aircraft.air_density * aircraft.cruise_speed ** 2

    return lift / (q * aircraft.wing_area)