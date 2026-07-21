"""
Optimization Objective Functions

Evaluates an aircraft design using aerodynamic performance,
flight safety, and geometric practicality.

The objective function converts several performance metrics
into one score between 0 and 100.

Mission-specific weighting allows different aircraft missions
to prioritize different performance characteristics.

Higher score = better overall design.
"""

from aerodynamics.drag import (
    drag_force,
    total_drag_coefficient,
)
from aerodynamics.lift import (
    required_cl,
    required_lift,
)
from aerodynamics.performance import (
    lift_to_drag_ratio,
    stall_speed,
    stall_speed_margin,
    wing_loading,
)


# ==========================================================
# Mission Weight Presets
# ==========================================================

GENERAL_WEIGHTS = {
    "required_cl": 0.25,
    "lift_to_drag": 0.30,
    "stall_margin": 0.25,
    "wing_loading": 0.15,
    "aspect_ratio": 0.05,
}


CARGO_WEIGHTS = {
    "required_cl": 0.20,
    "lift_to_drag": 0.25,
    "stall_margin": 0.25,
    "wing_loading": 0.25,
    "aspect_ratio": 0.05,
}


SURVEILLANCE_WEIGHTS = {
    "required_cl": 0.15,
    "lift_to_drag": 0.45,
    "stall_margin": 0.20,
    "wing_loading": 0.15,
    "aspect_ratio": 0.05,
}


GLIDER_WEIGHTS = {
    "required_cl": 0.15,
    "lift_to_drag": 0.55,
    "stall_margin": 0.15,
    "wing_loading": 0.10,
    "aspect_ratio": 0.05,
}


TRAINER_WEIGHTS = {
    "required_cl": 0.20,
    "lift_to_drag": 0.20,
    "stall_margin": 0.35,
    "wing_loading": 0.20,
    "aspect_ratio": 0.05,
}


RACING_WEIGHTS = {
    "required_cl": 0.30,
    "lift_to_drag": 0.20,
    "stall_margin": 0.20,
    "wing_loading": 0.20,
    "aspect_ratio": 0.10,
}


MISSION_WEIGHT_PRESETS = {
    "general": GENERAL_WEIGHTS,
    "cargo": CARGO_WEIGHTS,
    "surveillance": SURVEILLANCE_WEIGHTS,
    "glider": GLIDER_WEIGHTS,
    "trainer": TRAINER_WEIGHTS,
    "racing": RACING_WEIGHTS,
}


# ==========================================================
# Mission Weight Helper
# ==========================================================

def get_mission_weights(mission_name):
    """
    Return the objective weights for a specified mission.

    Parameters
    ----------
    mission_name : str
        Name of the aircraft mission.

    Returns
    -------
    dict
        Mission-specific objective weights.

    Raises
    ------
    ValueError
        If the mission name is not recognized.
    """

    normalized_name = mission_name.strip().lower()

    if normalized_name not in MISSION_WEIGHT_PRESETS:
        available_missions = ", ".join(MISSION_WEIGHT_PRESETS.keys())

        raise ValueError(
            f"Unknown mission '{mission_name}'. "
            f"Available missions: {available_missions}"
        )

    return MISSION_WEIGHT_PRESETS[normalized_name].copy()


def validate_mission_weights(mission_weights):
    """
    Validate a mission-weight dictionary.

    Parameters
    ----------
    mission_weights : dict
        Dictionary containing objective names and weights.

    Raises
    ------
    ValueError
        If required objective keys are missing, weights are
        negative, or the weights do not sum to 1.0.
    """

    required_keys = {
        "required_cl",
        "lift_to_drag",
        "stall_margin",
        "wing_loading",
        "aspect_ratio",
    }

    provided_keys = set(mission_weights.keys())

    missing_keys = required_keys - provided_keys
    extra_keys = provided_keys - required_keys

    if missing_keys:
        raise ValueError(
            "Mission weights are missing these objectives: "
            f"{sorted(missing_keys)}"
        )

    if extra_keys:
        raise ValueError(
            "Mission weights contain unknown objectives: "
            f"{sorted(extra_keys)}"
        )

    for objective_name, weight in mission_weights.items():
        if not isinstance(weight, (int, float)):
            raise TypeError(
                f"Weight for '{objective_name}' must be numeric."
            )

        if weight < 0.0:
            raise ValueError(
                f"Weight for '{objective_name}' cannot be negative."
            )

    weight_total = sum(mission_weights.values())

    if abs(weight_total - 1.0) > 1e-6:
        raise ValueError(
            "Mission weights must sum to 1.0. "
            f"Current total: {weight_total:.6f}"
        )


# ==========================================================
# Objective Function
# ==========================================================

def calculate_objective(
    wing,
    mass,
    gravity,
    air_density,
    cruise_speed,
    cl_max,
    mission_weights=None,
):
    """
    Calculate the optimization score and performance metrics
    for one aircraft design.

    Parameters
    ----------
    wing : Wing
        Wing geometry object being evaluated.

    mass : float
        Aircraft mass in kilograms.

    gravity : float
        Gravitational acceleration in m/s^2.

    air_density : float
        Air density in kg/m^3.

    cruise_speed : float
        Aircraft cruise speed in m/s.

    cl_max : float
        Maximum lift coefficient.

    mission_weights : dict, optional
        Mission-specific scoring weights.

        If no weights are supplied, GENERAL_WEIGHTS are used.

    Returns
    -------
    dict
        Dictionary containing the weighted objective score,
        category scores, and calculated performance metrics.
    """

    # --------------------------------------------------
    # Input validation
    # --------------------------------------------------

    if mass <= 0.0:
        raise ValueError("Aircraft mass must be greater than zero.")

    if gravity <= 0.0:
        raise ValueError("Gravity must be greater than zero.")

    if air_density <= 0.0:
        raise ValueError("Air density must be greater than zero.")

    if cruise_speed <= 0.0:
        raise ValueError("Cruise speed must be greater than zero.")

    if cl_max <= 0.0:
        raise ValueError("Maximum lift coefficient must be greater than zero.")

    if mission_weights is None:
        mission_weights = GENERAL_WEIGHTS.copy()
    else:
        mission_weights = mission_weights.copy()

    validate_mission_weights(mission_weights)

    # --------------------------------------------------
    # Wing geometry
    # --------------------------------------------------

    wing_area = wing.area
    aspect_ratio = wing.aspect_ratio()

    if wing_area <= 0.0:
        raise ValueError("Wing area must be greater than zero.")

    if aspect_ratio <= 0.0:
        raise ValueError("Aspect ratio must be greater than zero.")

    # --------------------------------------------------
    # Lift calculations
    # --------------------------------------------------

    weight = mass * gravity

    lift_required = required_lift(
        mass=mass,
        gravity=gravity,
    )

    required_cl_value = required_cl(
        mass=mass,
        gravity=gravity,
        air_density=air_density,
        velocity=cruise_speed,
        wing_area=wing_area,
    )

    # --------------------------------------------------
    # Drag calculations
    # --------------------------------------------------

    total_cd = total_drag_coefficient(
        cl=required_cl_value,
        aspect_ratio=aspect_ratio,
    )

    drag = drag_force(
        air_density=air_density,
        velocity=cruise_speed,
        wing_area=wing_area,
        cd=total_cd,
    )

    lift_drag = lift_to_drag_ratio(
        lift=lift_required,
        drag=drag,
    )

    # --------------------------------------------------
    # Performance calculations
    # --------------------------------------------------

    stall_speed_value = stall_speed(
        weight=weight,
        air_density=air_density,
        wing_area=wing_area,
        cl_max=cl_max,
    )

    stall_margin = stall_speed_margin(
        cruise_speed=cruise_speed,
        stall_speed_value=stall_speed_value,
    )

    wing_loading_value = wing_loading(
        weight=weight,
        wing_area=wing_area,
    )

    # --------------------------------------------------
    # Required CL score
    # Maximum raw score: 25 points
    # --------------------------------------------------

    if 0.30 <= required_cl_value <= 0.80:
        cl_score = 25.0
    elif 0.20 <= required_cl_value < 0.30:
        cl_score = 20.0
    elif 0.80 < required_cl_value <= 1.00:
        cl_score = 20.0
    elif 0.10 <= required_cl_value < 0.20:
        cl_score = 12.0
    elif 1.00 < required_cl_value <= 1.20:
        cl_score = 12.0
    else:
        cl_score = 0.0

    # --------------------------------------------------
    # Lift-to-drag score
    # Maximum raw score: 30 points
    # --------------------------------------------------

    if lift_drag >= 15.0:
        ld_score = 30.0
    elif lift_drag >= 12.0:
        ld_score = 26.0
    elif lift_drag >= 10.0:
        ld_score = 22.0
    elif lift_drag >= 8.0:
        ld_score = 17.0
    elif lift_drag >= 6.0:
        ld_score = 10.0
    else:
        ld_score = 3.0

    # --------------------------------------------------
    # Stall margin score
    # Maximum raw score: 25 points
    # --------------------------------------------------

    if stall_margin >= 1.60:
        stall_margin_score = 25.0
    elif stall_margin >= 1.50:
        stall_margin_score = 22.0
    elif stall_margin >= 1.40:
        stall_margin_score = 18.0
    elif stall_margin >= 1.30:
        stall_margin_score = 13.0
    elif stall_margin >= 1.20:
        stall_margin_score = 7.0
    else:
        stall_margin_score = 0.0

    # --------------------------------------------------
    # Wing loading score
    # Maximum raw score: 15 points
    # --------------------------------------------------

    if 50.0 <= wing_loading_value <= 90.0:
        wing_loading_score = 15.0
    elif 35.0 <= wing_loading_value < 50.0:
        wing_loading_score = 12.0
    elif 90.0 < wing_loading_value <= 110.0:
        wing_loading_score = 10.0
    elif 25.0 <= wing_loading_value < 35.0:
        wing_loading_score = 7.0
    elif 110.0 < wing_loading_value <= 130.0:
        wing_loading_score = 5.0
    else:
        wing_loading_score = 0.0

    # --------------------------------------------------
    # Aspect-ratio practicality score
    # Maximum raw score: 5 points
    # --------------------------------------------------

    if 6.0 <= aspect_ratio <= 12.0:
        aspect_ratio_score = 5.0
    elif 4.0 <= aspect_ratio < 6.0:
        aspect_ratio_score = 3.0
    elif 12.0 < aspect_ratio <= 15.0:
        aspect_ratio_score = 3.0
    else:
        aspect_ratio_score = 0.0

    # --------------------------------------------------
    # Normalize category scores
    #
    # Each category is converted to a value between 0 and 1.
    # This allows mission weights to be applied consistently.
    # --------------------------------------------------

    normalized_scores = {
        "required_cl": cl_score / 25.0,
        "lift_to_drag": ld_score / 30.0,
        "stall_margin": stall_margin_score / 25.0,
        "wing_loading": wing_loading_score / 15.0,
        "aspect_ratio": aspect_ratio_score / 5.0,
    }

    # --------------------------------------------------
    # Mission-weighted objective score
    # --------------------------------------------------

    weighted_score = 100.0 * sum(
        mission_weights[objective_name]
        * normalized_scores[objective_name]
        for objective_name in mission_weights
    )

    score_before_penalties = weighted_score

    # --------------------------------------------------
    # Hard feasibility penalties
    # --------------------------------------------------

    penalties = {}
    total_penalty = 0.0

    # Cruise must remain safely above stall speed.
    if stall_margin < 1.20:
        penalties["insufficient_stall_margin"] = 25.0
        total_penalty += 25.0

    # The required cruise CL should not approach or exceed CL max.
    if required_cl_value >= cl_max:
        penalties["required_cl_exceeds_cl_max"] = 30.0
        total_penalty += 30.0

    # Prevent nonphysical or numerically problematic results.
    if drag <= 0.0:
        penalties["nonpositive_drag"] = 100.0
        total_penalty += 100.0

    if lift_drag <= 0.0:
        penalties["nonpositive_lift_to_drag"] = 100.0
        total_penalty += 100.0

    weighted_score -= total_penalty

    # Keep the final score between 0 and 100.
    final_score = max(0.0, min(weighted_score, 100.0))

    feasible = len(penalties) == 0

    # --------------------------------------------------
    # Return all optimization data
    # --------------------------------------------------

    return {
        "score": round(final_score, 2),
        "score_before_penalties": round(score_before_penalties, 2),
        "total_penalty": round(total_penalty, 2),
        "feasible": feasible,
        "penalties": penalties,

        "wing_area": wing_area,
        "aspect_ratio": aspect_ratio,

        "required_lift": lift_required,
        "required_cl": required_cl_value,

        "total_cd": total_cd,
        "drag": drag,
        "lift_to_drag": lift_drag,

        "stall_speed": stall_speed_value,
        "stall_margin": stall_margin,
        "wing_loading": wing_loading_value,

        "cl_score": cl_score,
        "ld_score": ld_score,
        "stall_margin_score": stall_margin_score,
        "wing_loading_score": wing_loading_score,
        "aspect_ratio_score": aspect_ratio_score,

        "normalized_scores": normalized_scores,
        "mission_weights": mission_weights,
    }