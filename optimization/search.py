"""
Aircraft Design Search

Generates random wing designs within specified design bounds,
evaluates each design, and ranks the results from best to worst.

The search can use:

1. A mission-weighted aerodynamic objective score.
2. A mission-requirement score.
3. A combined final optimization score.
"""

import random

from geometry.wing import Wing
from missions.objective import mission_objective
from optimization.objectives import (
    calculate_objective,
    get_mission_weights,
)


# ==========================================================
# Random Design Generator
# ==========================================================

def generate_random_design(
    span_bounds,
    root_chord_bounds,
    tip_chord_bounds,
    cruise_speed_bounds,
    airfoil,
    sweep,
    dihedral,
):
    """
    Generate one random aircraft wing and cruise-speed design.

    Parameters
    ----------
    span_bounds : tuple
        Minimum and maximum wing span in meters.

    root_chord_bounds : tuple
        Minimum and maximum root chord in meters.

    tip_chord_bounds : tuple
        Minimum and maximum tip chord in meters.

    cruise_speed_bounds : tuple
        Minimum and maximum cruise speed in m/s.

    airfoil : str
        Airfoil designation.

    sweep : float
        Wing sweep angle in degrees.

    dihedral : float
        Wing dihedral angle in degrees.

    Returns
    -------
    tuple
        Wing object and randomly generated cruise speed.
    """

    span = random.uniform(
        span_bounds[0],
        span_bounds[1],
    )

    root_chord = random.uniform(
        root_chord_bounds[0],
        root_chord_bounds[1],
    )

    # The tip chord must not be larger than the root chord.
    allowed_tip_max = min(
        tip_chord_bounds[1],
        root_chord,
    )

    allowed_tip_min = min(
        tip_chord_bounds[0],
        allowed_tip_max,
    )

    tip_chord = random.uniform(
        allowed_tip_min,
        allowed_tip_max,
    )

    cruise_speed = random.uniform(
        cruise_speed_bounds[0],
        cruise_speed_bounds[1],
    )

    wing = Wing(
        span=span,
        root_chord=root_chord,
        tip_chord=tip_chord,
        airfoil=airfoil,
        sweep=sweep,
        dihedral=dihedral,
    )

    return wing, cruise_speed


# ==========================================================
# Search Input Validation
# ==========================================================

def validate_search_bounds(
    number_of_designs,
    span_bounds,
    root_chord_bounds,
    tip_chord_bounds,
    cruise_speed_bounds,
):
    """
    Validate the random-search inputs.
    """

    if number_of_designs <= 0:
        raise ValueError(
            "number_of_designs must be greater than zero."
        )

    bounds_to_check = {
        "span_bounds": span_bounds,
        "root_chord_bounds": root_chord_bounds,
        "tip_chord_bounds": tip_chord_bounds,
        "cruise_speed_bounds": cruise_speed_bounds,
    }

    for bounds_name, bounds in bounds_to_check.items():
        if len(bounds) != 2:
            raise ValueError(
                f"{bounds_name} must contain exactly two values."
            )

        minimum_value = bounds[0]
        maximum_value = bounds[1]

        if minimum_value <= 0.0:
            raise ValueError(
                f"The minimum value in {bounds_name} "
                "must be greater than zero."
            )

        if minimum_value >= maximum_value:
            raise ValueError(
                f"{bounds_name} must be written as "
                "(minimum, maximum)."
            )


# ==========================================================
# Random Design Search
# ==========================================================

def random_design_search(
    number_of_designs,
    span_bounds,
    root_chord_bounds,
    tip_chord_bounds,
    cruise_speed_bounds,
    airfoil,
    sweep,
    dihedral,
    mass,
    gravity,
    air_density,
    cl_max,
    random_seed=None,
    mission_requirements=None,
    mission_name="general",
    aerodynamic_weight=0.40,
    mission_weight=0.60,
):
    """
    Generate, evaluate, and rank random aircraft designs.

    Parameters
    ----------
    number_of_designs : int
        Number of random designs to evaluate.

    span_bounds : tuple
        Minimum and maximum wing span in meters.

    root_chord_bounds : tuple
        Minimum and maximum root chord in meters.

    tip_chord_bounds : tuple
        Minimum and maximum tip chord in meters.

    cruise_speed_bounds : tuple
        Minimum and maximum cruise speed in m/s.

    airfoil : str
        Airfoil designation.

    sweep : float
        Wing sweep angle in degrees.

    dihedral : float
        Wing dihedral angle in degrees.

    mass : float
        Aircraft mass in kilograms.

    gravity : float
        Gravitational acceleration in m/s^2.

    air_density : float
        Air density in kg/m^3.

    cl_max : float
        Maximum lift coefficient.

    random_seed : int or None
        Optional seed that makes random results repeatable.

    mission_requirements : dict or None
        Mission constraints used by mission_objective().

        When this is None, only the aerodynamic objective
        score is used.

    mission_name : str
        Name of the mission-weight preset used by the
        aerodynamic objective function.

        Available presets include:

        - general
        - cargo
        - surveillance
        - glider
        - trainer
        - racing

    aerodynamic_weight : float
        Contribution of the aerodynamic score to the final
        combined score.

    mission_weight : float
        Contribution of the mission score to the final
        combined score.

    Returns
    -------
    list
        Design dictionaries ranked from highest final score
        to lowest final score.
    """

    validate_search_bounds(
        number_of_designs=number_of_designs,
        span_bounds=span_bounds,
        root_chord_bounds=root_chord_bounds,
        tip_chord_bounds=tip_chord_bounds,
        cruise_speed_bounds=cruise_speed_bounds,
    )

    if mass <= 0.0:
        raise ValueError(
            "mass must be greater than zero."
        )

    if gravity <= 0.0:
        raise ValueError(
            "gravity must be greater than zero."
        )

    if air_density <= 0.0:
        raise ValueError(
            "air_density must be greater than zero."
        )

    if cl_max <= 0.0:
        raise ValueError(
            "cl_max must be greater than zero."
        )

    if aerodynamic_weight < 0.0:
        raise ValueError(
            "aerodynamic_weight cannot be negative."
        )

    if mission_weight < 0.0:
        raise ValueError(
            "mission_weight cannot be negative."
        )

    if mission_requirements is not None:
        combined_weight = aerodynamic_weight + mission_weight

        if abs(combined_weight - 1.0) > 1e-6:
            raise ValueError(
                "aerodynamic_weight and mission_weight "
                "must sum to 1.0."
            )

    if random_seed is not None:
        random.seed(random_seed)

    mission_weights = get_mission_weights(
        mission_name=mission_name,
    )

    results = []

    best_score_so_far = None

    for design_number in range(
        1,
        number_of_designs + 1,
    ):
        wing, cruise_speed = generate_random_design(
            span_bounds=span_bounds,
            root_chord_bounds=root_chord_bounds,
            tip_chord_bounds=tip_chord_bounds,
            cruise_speed_bounds=cruise_speed_bounds,
            airfoil=airfoil,
            sweep=sweep,
            dihedral=dihedral,
        )

        objective_result = calculate_objective(
            wing=wing,
            mass=mass,
            gravity=gravity,
            air_density=air_density,
            cruise_speed=cruise_speed,
            cl_max=cl_max,
            mission_weights=mission_weights,
        )

        aerodynamic_score = objective_result["score"]

        design_result = {
            "design_number": design_number,
            "wing": wing,
            "span": wing.span,
            "root_chord": wing.root_chord,
            "tip_chord": wing.tip_chord,
            "taper_ratio": (
                wing.tip_chord / wing.root_chord
            ),
            "cruise_speed": cruise_speed,
            "airfoil": airfoil,
            "sweep": sweep,
            "dihedral": dihedral,
            "mission_name": mission_name,
            "aerodynamic_score": aerodynamic_score,
            "generic_score": aerodynamic_score,
            **objective_result,
        }

        # --------------------------------------------------
        # Mission scoring
        # --------------------------------------------------

        if mission_requirements is not None:
            raw_mission_score = mission_objective(
                aircraft_results=design_result,
                mission_requirements=mission_requirements,
            )

            # The current mission objective is not naturally
            # limited to a 0-100 range. Clamp it temporarily
            # so it can be combined consistently.
            mission_score = max(
                0.0,
                min(raw_mission_score, 100.0),
            )

            combined_score = (
                aerodynamic_weight * aerodynamic_score
                + mission_weight * mission_score
            )

            design_result["raw_mission_score"] = round(
                raw_mission_score,
                2,
            )

            design_result["mission_score"] = round(
                mission_score,
                2,
            )

            design_result["score"] = round(
                combined_score,
                2,
            )

        else:
            design_result["raw_mission_score"] = None
            design_result["mission_score"] = None
            design_result["score"] = aerodynamic_score

        # --------------------------------------------------
        # Optimization history
        # --------------------------------------------------

        if (
            best_score_so_far is None
            or design_result["score"] > best_score_so_far
        ):
            best_score_so_far = design_result["score"]
            design_result["new_best"] = True
        else:
            design_result["new_best"] = False

        design_result["best_score_so_far"] = round(
            best_score_so_far,
            2,
        )

        results.append(design_result)

    # Rank designs from highest score to lowest score.
    results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    # Add final rank after sorting.
    for rank, result in enumerate(
        results,
        start=1,
    ):
        result["rank"] = rank

    return results