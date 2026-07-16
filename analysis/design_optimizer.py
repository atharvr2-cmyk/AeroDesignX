"""
Aircraft Design Optimizer

Generates and evaluates combinations of wing geometry
and flight conditions.
"""

from itertools import product

from aerodynamics.drag import (
    drag_force,
    total_drag_coefficient,
)
from aerodynamics.lift import required_cl
from aerodynamics.performance import (
    lift_to_drag_ratio,
    stall_speed,
    stall_speed_margin,
    wing_loading,
)
from geometry.wing import Wing


def calculate_design_score(
    required_cl_value,
    cl_max,
    lift_drag_value,
    stall_speed_value,
    stall_margin_value,
    wing_loading_value,
):
    """
    Calculate a continuous design score out of 100.

    Designs that cannot produce enough lift or that cruise
    too close to stall are rejected.
    """

    # Reject physically unacceptable designs
    if required_cl_value > cl_max:
        return 0.0

    if stall_margin_value < 1.3:
        return 0.0

    score = 0.0

    # Required CL: maximum 25 points
    cl_ratio = required_cl_value / cl_max
    score += max(0.0, 25.0 * (1.0 - cl_ratio))

    # Lift-to-drag ratio: maximum 35 points
    score += min(35.0, lift_drag_value / 15.0 * 35.0)

    # Stall margin: maximum 20 points
    score += min(
        20.0,
        max(
            0.0,
            (stall_margin_value - 1.3) / 0.7 * 20.0,
        ),
    )

    # Wing loading: maximum 20 points
    target_wing_loading = 90.0
    loading_error = abs(
        wing_loading_value - target_wing_loading
    )

    score += max(
        0.0,
        20.0 - loading_error / 4.0,
    )

    return round(score, 2)


def optimize_design(
    span_values,
    root_chord_values,
    tip_chord_values,
    cruise_speed_values,
    airfoil,
    sweep,
    dihedral,
    mass,
    gravity,
    air_density,
    cl_max,
):
    """
    Evaluate combinations of wing geometry and cruise speed.

    Returns
    -------
    list of dict
        All valid and invalid candidate designs.
    """

    results = []

    weight = mass * gravity

    combinations = product(
        span_values,
        root_chord_values,
        tip_chord_values,
        cruise_speed_values,
    )

    for (
        span,
        root_chord,
        tip_chord,
        cruise_speed,
    ) in combinations:

        # A tapered wing should not have a tip chord
        # larger than its root chord.
        if tip_chord > root_chord:
            continue

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

        required_cl_value = required_cl(
            mass=mass,
            gravity=gravity,
            air_density=air_density,
            velocity=cruise_speed,
            wing_area=wing_area,
        )

        total_cd_value = total_drag_coefficient(
            cl=required_cl_value,
            aspect_ratio=aspect_ratio,
        )

        drag_value = drag_force(
            air_density=air_density,
            velocity=cruise_speed,
            wing_area=wing_area,
            cd=total_cd_value,
        )

        lift_drag_value = lift_to_drag_ratio(
            lift=weight,
            drag=drag_value,
        )

        stall_speed_value = stall_speed(
            weight=weight,
            air_density=air_density,
            wing_area=wing_area,
            cl_max=cl_max,
        )

        stall_margin_value = stall_speed_margin(
            cruise_speed=cruise_speed,
            stall_speed_value=stall_speed_value,
        )

        wing_loading_value = wing_loading(
            weight=weight,
            wing_area=wing_area,
        )

        score = calculate_design_score(
            required_cl_value=required_cl_value,
            cl_max=cl_max,
            lift_drag_value=lift_drag_value,
            stall_speed_value=stall_speed_value,
            stall_margin_value=stall_margin_value,
            wing_loading_value=wing_loading_value,
        )

        results.append(
            {
                "span": span,
                "root_chord": root_chord,
                "tip_chord": tip_chord,
                "cruise_speed": cruise_speed,
                "wing_area": wing_area,
                "aspect_ratio": aspect_ratio,
                "required_cl": required_cl_value,
                "total_cd": total_cd_value,
                "drag": drag_value,
                "lift_to_drag": lift_drag_value,
                "stall_speed": stall_speed_value,
                "stall_margin": stall_margin_value,
                "wing_loading": wing_loading_value,
                "score": score,
            }
        )

    results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return results