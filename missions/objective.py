"""
Mission Objective Function

Scores an aircraft based on how well it satisfies
mission-specific performance requirements.

The final mission score remains between 0 and 100.

Higher score = better mission suitability.
"""


def calculate_ratio_score(
    actual_value,
    target_value,
    maximum_score,
    lower_is_better=False,
):
    """
    Calculate a normalized score based on a target value.

    Parameters
    ----------
    actual_value : float
        Performance value produced by the aircraft.

    target_value : float
        Desired or limiting mission value.

    maximum_score : float
        Maximum number of points available.

    lower_is_better : bool
        When True, values below the target receive the
        highest score.

    Returns
    -------
    float
        Score between 0 and maximum_score.
    """

    if target_value <= 0.0:
        raise ValueError(
            "target_value must be greater than zero."
        )

    if lower_is_better:
        if actual_value <= target_value:
            return maximum_score

        ratio = target_value / actual_value

    else:
        if actual_value >= target_value:
            return maximum_score

        ratio = actual_value / target_value

    ratio = max(
        0.0,
        min(ratio, 1.0),
    )

    return maximum_score * ratio


def mission_objective(
    aircraft_results,
    mission_requirements,
):
    """
    Compute a mission-specific objective score.

    Parameters
    ----------
    aircraft_results : dict
        Dictionary containing calculated aircraft
        performance metrics.

    mission_requirements : dict
        Dictionary containing mission constraints
        and desired performance targets.

    Returns
    -------
    float
        Mission suitability score between 0 and 100.
    """

    required_aircraft_keys = {
        "lift_to_drag",
        "stall_speed",
        "required_cl",
        "wing_loading",
    }

    missing_aircraft_keys = (
        required_aircraft_keys
        - set(aircraft_results.keys())
    )

    if missing_aircraft_keys:
        raise KeyError(
            "Aircraft results are missing: "
            f"{sorted(missing_aircraft_keys)}"
        )

    required_mission_keys = {
        "maximum_stall_speed",
    }

    missing_mission_keys = (
        required_mission_keys
        - set(mission_requirements.keys())
    )

    if missing_mission_keys:
        raise KeyError(
            "Mission requirements are missing: "
            f"{sorted(missing_mission_keys)}"
        )

    score = 0.0

    # ======================================================
    # Aerodynamic Efficiency
    # Maximum: 30 points
    # ======================================================

    lift_to_drag = aircraft_results[
        "lift_to_drag"
    ]

    target_lift_to_drag = mission_requirements.get(
        "minimum_lift_to_drag",
        12.0,
    )

    efficiency_score = calculate_ratio_score(
        actual_value=lift_to_drag,
        target_value=target_lift_to_drag,
        maximum_score=30.0,
        lower_is_better=False,
    )

    score += efficiency_score

    # ======================================================
    # Stall Speed
    # Maximum: 30 points
    # ======================================================

    stall_speed = aircraft_results[
        "stall_speed"
    ]

    maximum_stall_speed = mission_requirements[
        "maximum_stall_speed"
    ]

    stall_speed_score = calculate_ratio_score(
        actual_value=stall_speed,
        target_value=maximum_stall_speed,
        maximum_score=30.0,
        lower_is_better=True,
    )

    score += stall_speed_score

    # ======================================================
    # Cruise Lift Coefficient
    # Maximum: 20 points
    #
    # A required CL near the preferred value is rewarded.
    # ======================================================

    required_cl = aircraft_results[
        "required_cl"
    ]

    preferred_cl = mission_requirements.get(
        "preferred_cruise_cl",
        0.60,
    )

    maximum_cl_difference = mission_requirements.get(
        "maximum_cl_difference",
        0.60,
    )

    cl_difference = abs(
        required_cl - preferred_cl
    )

    cl_score_fraction = (
        1.0
        - cl_difference / maximum_cl_difference
    )

    cl_score_fraction = max(
        0.0,
        min(cl_score_fraction, 1.0),
    )

    cruise_cl_score = (
        20.0 * cl_score_fraction
    )

    score += cruise_cl_score

    # ======================================================
    # Wing Loading
    # Maximum: 20 points
    #
    # Designs closer to the preferred loading receive
    # more points.
    # ======================================================

    wing_loading = aircraft_results[
        "wing_loading"
    ]

    preferred_wing_loading = (
        mission_requirements.get(
            "preferred_wing_loading",
            90.0,
        )
    )

    wing_loading_tolerance = (
        mission_requirements.get(
            "wing_loading_tolerance",
            60.0,
        )
    )

    loading_difference = abs(
        wing_loading
        - preferred_wing_loading
    )

    loading_score_fraction = (
        1.0
        - loading_difference
        / wing_loading_tolerance
    )

    loading_score_fraction = max(
        0.0,
        min(loading_score_fraction, 1.0),
    )

    wing_loading_score = (
        20.0 * loading_score_fraction
    )

    score += wing_loading_score

    # ======================================================
    # Hard Mission Penalties
    # ======================================================

    penalty = 0.0

    # Apply a penalty when stall speed exceeds
    # the mission limit.
    if stall_speed > maximum_stall_speed:
        excess_fraction = (
            stall_speed
            - maximum_stall_speed
        ) / maximum_stall_speed

        penalty += min(
            30.0,
            excess_fraction * 50.0,
        )

    # Apply a penalty when the required cruise CL
    # is physically unreasonable.
    cl_max = mission_requirements.get(
        "cl_max",
    )

    if (
        cl_max is not None
        and required_cl >= cl_max
    ):
        penalty += 30.0

    final_score = score - penalty

    final_score = max(
        0.0,
        min(final_score, 100.0),
    )

    return round(
        final_score,
        2,
    )