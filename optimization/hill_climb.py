"""
Hill Climbing Optimizer

Improves an existing aircraft design by making small,
controlled changes to its geometry and cruise speed.
"""

import random

from geometry.wing import Wing
from missions.objective import mission_objective
from optimization.objectives import calculate_objective


def perturb(value, fraction):
    """
    Randomly adjust a value within a specified fraction.
    """

    return value * random.uniform(
        1.0 - fraction,
        1.0 + fraction,
    )


def clamp(value, bounds):
    """
    Keep a value inside its permitted bounds.
    """

    minimum, maximum = bounds

    return max(
        minimum,
        min(value, maximum),
    )


def hill_climb(
    initial_design,
    mass,
    gravity,
    air_density,
    cl_max,
    iterations=100,
    mission_weights=None,
    mission_requirements=None,
    aerodynamic_weight=0.40,
    mission_weight=0.60,
    span_bounds=None,
    root_chord_bounds=None,
    tip_chord_bounds=None,
    cruise_speed_bounds=None,
    random_seed=None,
):
    """
    Improve an aircraft design using hill climbing.

    Returns
    -------
    dict
        Improved aircraft design with optimization history.
    """

    if random_seed is not None:
        random.seed(random_seed)

    best = initial_design.copy()

    initial_score = best["score"]

    history = [
        {
            "iteration": 0,
            "score": best["score"],
            "aerodynamic_score": best.get(
                "aerodynamic_score",
                best["score"],
            ),
            "mission_score": best.get(
                "mission_score",
            ),
            "accepted": True,
        }
    ]

    accepted_changes = 0

    for iteration in range(1, iterations + 1):

        candidate_span = perturb(
            best["span"],
            0.04,
        )

        candidate_root_chord = perturb(
            best["root_chord"],
            0.04,
        )

        candidate_tip_chord = perturb(
            best["tip_chord"],
            0.04,
        )

        candidate_cruise_speed = perturb(
            best["cruise_speed"],
            0.025,
        )

        if span_bounds is not None:
            candidate_span = clamp(
                candidate_span,
                span_bounds,
            )

        if root_chord_bounds is not None:
            candidate_root_chord = clamp(
                candidate_root_chord,
                root_chord_bounds,
            )

        if tip_chord_bounds is not None:
            candidate_tip_chord = clamp(
                candidate_tip_chord,
                tip_chord_bounds,
            )

        if cruise_speed_bounds is not None:
            candidate_cruise_speed = clamp(
                candidate_cruise_speed,
                cruise_speed_bounds,
            )

        # Ensure the tip chord does not exceed the root chord.
        candidate_tip_chord = min(
            candidate_tip_chord,
            candidate_root_chord,
        )

        candidate_wing = Wing(
            span=candidate_span,
            root_chord=candidate_root_chord,
            tip_chord=candidate_tip_chord,
            sweep=best["sweep"],
            dihedral=best["dihedral"],
            airfoil=best["airfoil"],
        )

        objective_result = calculate_objective(
            wing=candidate_wing,
            cruise_speed=candidate_cruise_speed,
            mass=mass,
            gravity=gravity,
            air_density=air_density,
            cl_max=cl_max,
            mission_weights=mission_weights,
        )

        aerodynamic_score = objective_result["score"]

        if mission_requirements is not None:
            mission_result = mission_objective(
                objective_result,
                mission_requirements,
            )

            if isinstance(mission_result, dict):
                mission_score = mission_result["score"]
                raw_mission_score = mission_result.get(
                    "raw_score",
                    mission_score,
                )
            else:
                mission_score = mission_result
                raw_mission_score = mission_result

            candidate_score = (
                aerodynamic_weight
                * aerodynamic_score
                + mission_weight
                * mission_score
            )

        else:
            mission_score = None
            raw_mission_score = None
            candidate_score = aerodynamic_score

        accepted = candidate_score > best["score"]

        if accepted:
            accepted_changes += 1

            best.update(objective_result)

            best.update(
                {
                    "wing": candidate_wing,
                    "span": candidate_wing.span,
                    "root_chord": candidate_wing.root_chord,
                    "tip_chord": candidate_wing.tip_chord,
                    "taper_ratio": (
                        candidate_wing.tip_chord
                        / candidate_wing.root_chord
                    ),
                    "wing_area": candidate_wing.area,
                    "aspect_ratio": (
                        candidate_wing.aspect_ratio()
                    ),
                    "cruise_speed": (
                        candidate_cruise_speed
                    ),
                    "aerodynamic_score": (
                        aerodynamic_score
                    ),
                    "generic_score": (
                        aerodynamic_score
                    ),
                    "mission_score": mission_score,
                    "raw_mission_score": (
                        raw_mission_score
                    ),
                    "score": candidate_score,
                }
            )

        history.append(
            {
                "iteration": iteration,
                "score": best["score"],
                "aerodynamic_score": best.get(
                    "aerodynamic_score",
                    best["score"],
                ),
                "mission_score": best.get(
                    "mission_score",
                ),
                "accepted": accepted,
            }
        )

    best["hill_climb_initial_score"] = initial_score
    best["hill_climb_final_score"] = best["score"]

    best["hill_climb_improvement"] = (
        best["score"] - initial_score
    )

    best["hill_climb_iterations"] = iterations
    best["accepted_changes"] = accepted_changes
    best["optimization_history"] = history

    return best