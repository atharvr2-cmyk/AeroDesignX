"""
Aircraft Parameter Sweep

Evaluates how changes in aircraft geometry affect aerodynamic performance.
"""

import numpy as np

from aerodynamics.drag import (
    drag_force,
    total_drag_coefficient,
)
from aerodynamics.lift import required_cl
from aerodynamics.performance import (
    lift_to_drag_ratio,
    stall_speed,
    wing_loading,
)
from geometry.wing import Wing


def sweep_wing_span(
    span_values,
    root_chord,
    tip_chord,
    airfoil,
    sweep,
    dihedral,
    mass,
    gravity,
    air_density,
    cruise_speed,
    cl_max,
):
    """
    Evaluate aircraft performance over a range of wing spans.

    Parameters
    ----------
    span_values : iterable
        Wing spans to test in meters.

    Returns
    -------
    list of dict
        Performance results for each wing span.
    """

    results = []

    weight = mass * gravity

    for span in span_values:
        wing = Wing(
            span=span,
            root_chord=root_chord,
            tip_chord=tip_chord,
            airfoil=airfoil,
            sweep=sweep,
            dihedral=dihedral,
        )

        wing_area = wing.area
        aspect_ratio = wing.aspect_ratio()

        cl_required = required_cl(
            mass=mass,
            gravity=gravity,
            air_density=air_density,
            velocity=cruise_speed,
            wing_area=wing_area,
        )

        cd_total = total_drag_coefficient(
            cl=cl_required,
            aspect_ratio=aspect_ratio,
        )

        drag = drag_force(
            air_density=air_density,
            velocity=cruise_speed,
            wing_area=wing_area,
            cd=cd_total,
        )

        lift_drag = lift_to_drag_ratio(
            lift=weight,
            drag=drag,
        )

        stall_speed_value = stall_speed(
            weight=weight,
            air_density=air_density,
            wing_area=wing_area,
            cl_max=cl_max,
        )

        wing_loading_value = wing_loading(
            weight=weight,
            wing_area=wing_area,
        )

        result = {
            "span": span,
            "wing_area": wing_area,
            "aspect_ratio": aspect_ratio,
            "required_cl": cl_required,
            "total_cd": cd_total,
            "drag": drag,
            "lift_to_drag": lift_drag,
            "stall_speed": stall_speed_value,
            "wing_loading": wing_loading_value,
        }

        result["score"] = score_sweep_result(result)

        results.append(result)

    return results


def score_sweep_result(result):
    """
    Assign an overall design score to one parameter-sweep result.

    The score considers:
    - Required lift coefficient
    - Lift-to-drag ratio
    - Stall speed
    - Wing loading

    Parameters
    ----------
    result : dict
        Performance values for one wing design.

    Returns
    -------
    int
        Overall score out of 100.
    """

    score = 0

    required_cl_value = result["required_cl"]
    lift_drag_value = result["lift_to_drag"]
    stall_speed_value = result["stall_speed"]
    wing_loading_value = result["wing_loading"]

    # Required CL: maximum 30 points
    if required_cl_value <= 0.8:
        score += 30
    elif required_cl_value <= 1.0:
        score += 24
    elif required_cl_value <= 1.2:
        score += 16
    else:
        score += 5

    # Lift-to-drag ratio: maximum 30 points
    if lift_drag_value >= 15:
        score += 30
    elif lift_drag_value >= 12:
        score += 25
    elif lift_drag_value >= 9:
        score += 20
    elif lift_drag_value >= 7:
        score += 12
    else:
        score += 5

    # Stall speed: maximum 25 points
    if stall_speed_value <= 7:
        score += 25
    elif stall_speed_value <= 9:
        score += 20
    elif stall_speed_value <= 11:
        score += 14
    else:
        score += 5

    # Wing loading: maximum 15 points
    if 60 <= wing_loading_value <= 100:
        score += 15
    elif 40 <= wing_loading_value < 60:
        score += 11
    elif 100 < wing_loading_value <= 130:
        score += 10
    else:
        score += 5

    return score