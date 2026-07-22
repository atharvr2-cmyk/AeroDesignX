"""
Mission Evaluator

Evaluates an AeroDesignX optimization result against a selected mission.
"""


def evaluate_mission(
    aircraft_results,
    mission_requirements,
    estimated_endurance_hours=None,
    estimated_range_km=None,
):
    """
    Evaluate an optimized aircraft design against mission requirements.

    Parameters
    ----------
    aircraft_results : dict
        Dictionary returned by the AeroDesignX optimizer.

    mission_requirements : dict
        Dictionary returned by calculate_mission_requirements().

    estimated_endurance_hours : float, optional
        Estimated aircraft endurance in hours.

    estimated_range_km : float, optional
        Estimated aircraft range in kilometers.

    Returns
    -------
    dict
        Mission score, feasibility status, penalties, and comments.
    """

    score = 100.0
    comments = []
    penalties = {}
    failed_constraints = []

    # ----------------------------------------------------------
    # Stall-speed requirement
    # ----------------------------------------------------------

    actual_stall_speed = aircraft_results["stall_speed"]
    maximum_stall_speed = mission_requirements.get(
        "maximum_stall_speed",
        mission_requirements.get("stall_speed"),
    )

    if actual_stall_speed <= maximum_stall_speed:
        penalties["stall_speed"] = 0.0
        comments.append("Stall-speed requirement satisfied.")
    else:
        difference = actual_stall_speed - maximum_stall_speed
        penalty = difference * 8.0

        score -= penalty
        penalties["stall_speed"] = penalty
        failed_constraints.append("stall_speed")

        comments.append(
            f"Stall speed is {difference:.2f} m/s above the mission limit."
        )

    # ----------------------------------------------------------
    # Required lift-coefficient check
    # ----------------------------------------------------------
    # A very high required CL indicates that the wing must operate
    # too close to stall during normal flight.

    required_cl = aircraft_results["required_cl"]
    maximum_cruise_cl = 1.0

    if required_cl <= maximum_cruise_cl:
        penalties["required_cl"] = 0.0
        comments.append("Cruise lift coefficient is acceptable.")
    else:
        difference = required_cl - maximum_cruise_cl
        penalty = difference * 20.0

        score -= penalty
        penalties["required_cl"] = penalty
        failed_constraints.append("required_cl")

        comments.append(
            f"Required CL exceeds the recommended cruise limit by "
            f"{difference:.3f}."
        )

    # ----------------------------------------------------------
    # Aerodynamic-efficiency check
    # ----------------------------------------------------------

    lift_to_drag = aircraft_results["lift_to_drag"]

    if lift_to_drag >= 12.0:
        penalties["efficiency"] = 0.0
        comments.append("Aerodynamic efficiency is excellent.")

    elif lift_to_drag >= 8.0:
        penalty = (12.0 - lift_to_drag) * 1.5

        score -= penalty
        penalties["efficiency"] = penalty

        comments.append("Aerodynamic efficiency is acceptable.")

    else:
        penalty = (8.0 - lift_to_drag) * 4.0 + 6.0

        score -= penalty
        penalties["efficiency"] = penalty
        failed_constraints.append("efficiency")

        comments.append("Aerodynamic efficiency is below the mission target.")

    # ----------------------------------------------------------
    # Endurance requirement
    # ----------------------------------------------------------

    required_endurance = mission_requirements.get(
        "endurance_with_reserve_hours",
        mission_requirements.get("endurance_hr"),
    )

    if estimated_endurance_hours is None:
        penalties["endurance"] = 0.0
        comments.append(
            "Endurance was not evaluated because no estimate was supplied."
        )

    elif estimated_endurance_hours >= required_endurance:
        penalties["endurance"] = 0.0
        comments.append("Endurance requirement satisfied.")

    else:
        difference = required_endurance - estimated_endurance_hours
        penalty = difference * 15.0

        score -= penalty
        penalties["endurance"] = penalty
        failed_constraints.append("endurance")

        comments.append(
            f"Endurance is {difference:.2f} hr below the requirement."
        )

    # ----------------------------------------------------------
    # Range requirement
    # ----------------------------------------------------------

    required_range = mission_requirements.get(
        "required_range_km",
        mission_requirements.get("range_km"),
    )

    if estimated_range_km is None:
        penalties["range"] = 0.0
        comments.append(
            "Range was not evaluated because no estimate was supplied."
        )

    elif estimated_range_km >= required_range:
        penalties["range"] = 0.0
        comments.append("Range requirement satisfied.")

    else:
        difference = required_range - estimated_range_km
        percentage_shortfall = difference / required_range
        penalty = percentage_shortfall * 25.0

        score -= penalty
        penalties["range"] = penalty
        failed_constraints.append("range")

        comments.append(
            f"Range is {difference:.1f} km below the requirement."
        )

    # ----------------------------------------------------------
    # Final result
    # ----------------------------------------------------------

    score = max(0.0, min(100.0, score))

    feasible = len(failed_constraints) == 0

    return {
        "mission": mission_requirements.get(
            "mission_name",
            mission_requirements.get("name", "Custom Mission"),
        ),
        "score": score,
        "feasible": feasible,
        "failed_constraints": failed_constraints,
        "penalties": penalties,
        "comments": comments,
    }


def print_mission_evaluation(evaluation):
    """
    Print a formatted mission-evaluation report.
    """

    print()
    print("=" * 72)
    print("MISSION EVALUATION")
    print("=" * 72)

    print(f"Mission:          {evaluation['mission']}")
    print(f"Mission Score:    {evaluation['score']:.1f}/100")

    if evaluation["feasible"]:
        print("Feasibility:      PASS")
    else:
        print("Feasibility:      FAIL")

    print()
    print("ASSESSMENT")
    print("-" * 72)

    for comment in evaluation["comments"]:
        print(f"- {comment}")

    if evaluation["failed_constraints"]:
        print()
        print("FAILED CONSTRAINTS")
        print("-" * 72)

        for constraint in evaluation["failed_constraints"]:
            readable_name = constraint.replace("_", " ").title()
            print(f"- {readable_name}")

    print("=" * 72)