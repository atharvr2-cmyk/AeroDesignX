"""
Aircraft Design Optimizer

Runs a random aircraft design search, reports optimization
progress, prints the highest-ranked aircraft concepts, and
returns the best design.
"""

from optimization.search import random_design_search
from optimization.hill_climb import hill_climb


def optimize_aircraft(
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
    top_n=10,
    random_seed=None,
    mission_requirements=None,
    mission_name="general",
    aerodynamic_weight=0.40,
    mission_weight=0.60,
):
    """
    Run the random aircraft design optimization.

    Parameters
    ----------
    number_of_designs : int
        Number of random aircraft designs to evaluate.

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

    top_n : int
        Number of highest-ranked designs to print.

    random_seed : int or None
        Optional seed used to make results repeatable.

    mission_requirements : dict or None
        Optional mission requirements. When supplied, designs
        are ranked using combined aerodynamic and mission scores.

    mission_name : str
        Mission-weight preset used by the aerodynamic objective.

        Available presets:

        - general
        - cargo
        - surveillance
        - glider
        - trainer
        - racing

    aerodynamic_weight : float
        Contribution of the aerodynamic score to the combined
        optimization score.

    mission_weight : float
        Contribution of the mission score to the combined
        optimization score.

    Returns
    -------
    dict
        Highest-ranked aircraft design.
    """

    # ======================================================
    # Run design search
    # ======================================================

    results = random_design_search(
        number_of_designs=number_of_designs,
        span_bounds=span_bounds,
        root_chord_bounds=root_chord_bounds,
        tip_chord_bounds=tip_chord_bounds,
        cruise_speed_bounds=cruise_speed_bounds,
        airfoil=airfoil,
        sweep=sweep,
        dihedral=dihedral,
        mass=mass,
        gravity=gravity,
        air_density=air_density,
        cl_max=cl_max,
        random_seed=random_seed,
        mission_requirements=mission_requirements,
        mission_name=mission_name,
        aerodynamic_weight=aerodynamic_weight,
        mission_weight=mission_weight,
    )

    if not results:
        raise RuntimeError(
            "The aircraft optimization produced no results."
        )

    number_to_show = min(
        top_n,
        len(results),
    )

    best_design = results[0]

    random_best_design = best_design.copy()

    # ======================================================
    # Improve the best design using hill climbing
    # ======================================================

    best_design = hill_climb(
        initial_design=random_best_design,
        mass=mass,
        gravity=gravity,
        air_density=air_density,
        cl_max=cl_max,
        iterations=100,
        mission_weights=random_best_design.get(
            "mission_weights",
        ),
        mission_requirements=mission_requirements,
        aerodynamic_weight=aerodynamic_weight,
        mission_weight=mission_weight,
        span_bounds=span_bounds,
        root_chord_bounds=root_chord_bounds,
        tip_chord_bounds=tip_chord_bounds,
        cruise_speed_bounds=cruise_speed_bounds,
        random_seed=random_seed,
    )

    # Results are ranked after the search, so recover the
    # original iteration order using design_number.
    iteration_results = sorted(
        results,
        key=lambda result: result["design_number"],
    )

    first_design = iteration_results[0]

    initial_score = first_design["score"]
    final_score = best_design["score"]

    score_improvement = (
        final_score - initial_score
    )

    feasible_designs = sum(
        1
        for result in results
        if result.get("feasible", False)
    )

    infeasible_designs = (
        len(results) - feasible_designs
    )

    improvement_count = sum(
        1
        for result in results
        if result.get("new_best", False)
    )

    feasible_percentage = (
        100.0
        * feasible_designs
        / len(results)
    )

    # ======================================================
    # Main optimization summary
    # ======================================================

    print("\n" + "=" * 132)
    print("MISSION-AWARE AIRCRAFT DESIGN OPTIMIZATION")
    print("=" * 132)

    if mission_requirements is not None:
        mission_display_name = mission_requirements.get(
            "mission_name",
            mission_name.title(),
        )

        print(
            f"Optimization mission:       "
            f"{mission_display_name}"
        )

        print(
            f"Mission weight preset:      "
            f"{mission_name.title()}"
        )

        print(
            f"Scoring mode:               "
            f"Combined aerodynamic and mission scoring"
        )

        print(
            f"Aerodynamic contribution:   "
            f"{aerodynamic_weight * 100.0:.0f}%"
        )

        print(
            f"Mission contribution:       "
            f"{mission_weight * 100.0:.0f}%"
        )

    else:
        print(
            f"Optimization mission:       "
            f"General aircraft"
        )

        print(
            f"Mission weight preset:      "
            f"{mission_name.title()}"
        )

        print(
            f"Scoring mode:               "
            f"Aerodynamic scoring only"
        )

    print(
        f"Designs evaluated:          "
        f"{len(results)}"
    )

    print(
        f"Feasible designs:           "
        f"{feasible_designs} "
        f"({feasible_percentage:.1f}%)"
    )

    print(
        f"Infeasible designs:         "
        f"{infeasible_designs}"
    )

    print(
        f"New best designs found:     "
        f"{improvement_count}"
    )

    # ======================================================
    # Optimization progress
    # ======================================================

    print("\nOPTIMIZATION PROGRESS")
    print("-" * 72)

    print(
        f"First generated score:      "
        f"{initial_score:.2f}/100"
    )

    print(
    f"Best random-search score:   "
    f"{random_best_design['score']:.2f}/100"
    )

    random_search_improvement = (
        random_best_design["score"]
        - initial_score
    )

    print(
        f"Random-search improvement:  "
        f"{random_search_improvement:+.2f} points"
    )

    print(
    f"Best random design found at:"
    f" Iteration "
    f"{random_best_design['design_number']}"
    )

    print("\nHILL-CLIMB REFINEMENT")
    print("-" * 72)

    print(
        f"Best random-search score:   "
        f"{best_design['hill_climb_initial_score']:.2f}/100"
    )

    print(
        f"Refined hill-climb score:   "
        f"{best_design['hill_climb_final_score']:.2f}/100"
    )

    print(
        f"Hill-climb improvement:     "
        f"{best_design['hill_climb_improvement']:+.2f} points"
    )

    print(
        f"Hill-climb iterations:      "
        f"{best_design['hill_climb_iterations']}"
    )

    print(
        f"Accepted improvements:      "
        f"{best_design['accepted_changes']}"
    )

    # ======================================================
    # Hill-climb convergence history
    # ======================================================

    optimization_history = best_design.get(
        "optimization_history",
        [],
    )

    if optimization_history:
        print("\nHILL-CLIMB CONVERGENCE")
        print("-" * 72)

        history_length = len(optimization_history)

        sample_iterations = [
            0,
            10,
            20,
            30,
            40,
            50,
            60,
            70,
            80,
            90,
            100,
        ]

        print(
            f"{'Iteration':<14}"
            f"{'Best Score':<16}"
            f"{'Accepted?':<12}"
        )

        print("-" * 42)

        for sample_iteration in sample_iterations:
            if sample_iteration < history_length:
                history_entry = optimization_history[
                    sample_iteration
                ]

                accepted_text = (
                    "YES"
                    if history_entry["accepted"]
                    else "NO"
                )

                print(
                    f"{history_entry['iteration']:<14}"
                    f"{history_entry['score']:<16.2f}"
                    f"{accepted_text:<12}"
                )

    # ======================================================
    # Top-ranked design table
    # ======================================================

    print("\nTOP-RANKED AIRCRAFT DESIGNS")
    print("-" * 132)

    if mission_requirements is not None:
        print(
            f"{'Rank':<6}"
            f"{'Design':<8}"
            f"{'Final':<9}"
            f"{'Aero':<9}"
            f"{'Mission':<10}"
            f"{'Span':<9}"
            f"{'Root':<9}"
            f"{'Tip':<9}"
            f"{'Speed':<10}"
            f"{'Area':<10}"
            f"{'AR':<8}"
            f"{'CL Req.':<10}"
            f"{'L/D':<9}"
            f"{'Stall':<9}"
        )

    else:
        print(
            f"{'Rank':<7}"
            f"{'Design':<9}"
            f"{'Score':<9}"
            f"{'Span':<9}"
            f"{'Root':<9}"
            f"{'Tip':<9}"
            f"{'Speed':<10}"
            f"{'Area':<10}"
            f"{'AR':<9}"
            f"{'CL Req.':<10}"
            f"{'L/D':<9}"
            f"{'Stall':<9}"
            f"{'Feasible':<10}"
        )

    print("-" * 132)

    for result in results[:number_to_show]:
        if mission_requirements is not None:
            mission_score = result.get(
                "mission_score",
                0.0,
            )

            print(
                f"{result['rank']:<6}"
                f"{result['design_number']:<8}"
                f"{result['score']:<9.2f}"
                f"{result['aerodynamic_score']:<9.2f}"
                f"{mission_score:<10.2f}"
                f"{result['span']:<9.3f}"
                f"{result['root_chord']:<9.3f}"
                f"{result['tip_chord']:<9.3f}"
                f"{result['cruise_speed']:<10.2f}"
                f"{result['wing_area']:<10.3f}"
                f"{result['aspect_ratio']:<8.2f}"
                f"{result['required_cl']:<10.3f}"
                f"{result['lift_to_drag']:<9.2f}"
                f"{result['stall_speed']:<9.2f}"
            )

        else:
            feasible_text = (
                "YES"
                if result.get("feasible", False)
                else "NO"
            )

            print(
                f"{result['rank']:<7}"
                f"{result['design_number']:<9}"
                f"{result['score']:<9.2f}"
                f"{result['span']:<9.3f}"
                f"{result['root_chord']:<9.3f}"
                f"{result['tip_chord']:<9.3f}"
                f"{result['cruise_speed']:<10.2f}"
                f"{result['wing_area']:<10.3f}"
                f"{result['aspect_ratio']:<9.2f}"
                f"{result['required_cl']:<10.3f}"
                f"{result['lift_to_drag']:<9.2f}"
                f"{result['stall_speed']:<9.2f}"
                f"{feasible_text:<10}"
            )

    print("=" * 132)

    # ======================================================
    # Best design score summary
    # ======================================================

    print("\nBEST RANDOMLY GENERATED DESIGN")
    print("-" * 72)

    print(
        f"Design number:              "
        f"{best_design['design_number']}"
    )

    if mission_requirements is not None:
        print(
            f"Mission:                    "
            f"{mission_display_name}"
        )

        print(
            f"Aerodynamic score:          "
            f"{best_design['aerodynamic_score']:.2f}/100"
        )

        print(
            f"Mission score:              "
            f"{best_design['mission_score']:.2f}/100"
        )

        print(
            f"Combined optimization score:"
            f" {best_design['score']:.2f}/100"
        )

    else:
        print(
            f"Optimization score:         "
            f"{best_design['score']:.2f}/100"
        )

    feasible_text = (
        "PASS"
        if best_design.get("feasible", False)
        else "FAIL"
    )

    print(
        f"Aerodynamic feasibility:    "
        f"{feasible_text}"
    )

    print(
        f"Score before penalties:     "
        f"{best_design.get('score_before_penalties', 0.0):.2f}/100"
    )

    print(
        f"Total aerodynamic penalty:  "
        f"{best_design.get('total_penalty', 0.0):.2f}"
    )

    # ======================================================
    # Best design geometry
    # ======================================================

    print("\nOPTIMIZED GEOMETRY")
    print("-" * 72)

    print(
        f"Wing span:                  "
        f"{best_design['span']:.3f} m"
    )

    print(
        f"Root chord:                 "
        f"{best_design['root_chord']:.3f} m"
    )

    print(
        f"Tip chord:                  "
        f"{best_design['tip_chord']:.3f} m"
    )

    print(
        f"Taper ratio:                "
        f"{best_design.get('taper_ratio', 0.0):.3f}"
    )

    print(
        f"Wing area:                  "
        f"{best_design['wing_area']:.3f} m^2"
    )

    print(
        f"Aspect ratio:               "
        f"{best_design['aspect_ratio']:.2f}"
    )

    print(
        f"Sweep angle:                "
        f"{best_design['sweep']:.2f} deg"
    )

    print(
        f"Dihedral angle:             "
        f"{best_design['dihedral']:.2f} deg"
    )

    print(
        f"Airfoil:                    "
        f"{best_design['airfoil']}"
    )

    # ======================================================
    # Best design performance
    # ======================================================

    print("\nPREDICTED PERFORMANCE")
    print("-" * 72)

    print(
        f"Cruise speed:               "
        f"{best_design['cruise_speed']:.2f} m/s"
    )

    print(
        f"Required lift coefficient:  "
        f"{best_design['required_cl']:.3f}"
    )

    print(
        f"Total drag coefficient:     "
        f"{best_design['total_cd']:.4f}"
    )

    print(
        f"Drag force:                 "
        f"{best_design['drag']:.2f} N"
    )

    print(
        f"Lift-to-drag ratio:         "
        f"{best_design['lift_to_drag']:.2f}"
    )

    print(
        f"Stall speed:                "
        f"{best_design['stall_speed']:.2f} m/s"
    )

    print(
        f"Stall-speed margin:         "
        f"{best_design['stall_margin']:.2f}"
    )

    print(
        f"Wing loading:               "
        f"{best_design['wing_loading']:.2f} N/m^2"
    )

    # ======================================================
    # Raw category breakdown
    # ======================================================

    print("\nAERODYNAMIC CATEGORY BREAKDOWN")
    print("-" * 72)

    print(
        f"Required CL score:          "
        f"{best_design['cl_score']:.1f}/25"
    )

    print(
        f"L/D score:                  "
        f"{best_design['ld_score']:.1f}/30"
    )

    print(
        f"Stall-margin score:         "
        f"{best_design['stall_margin_score']:.1f}/25"
    )

    print(
        f"Wing-loading score:         "
        f"{best_design['wing_loading_score']:.1f}/15"
    )

    print(
        f"Aspect-ratio score:         "
        f"{best_design['aspect_ratio_score']:.1f}/5"
    )

    # ======================================================
    # Mission-weight information
    # ======================================================

    mission_weights = best_design.get(
        "mission_weights",
        {},
    )

    if mission_weights:
        print("\nMISSION-WEIGHTED PRIORITIES")
        print("-" * 72)

        print(
            f"Required CL importance:     "
            f"{mission_weights['required_cl'] * 100.0:.0f}%"
        )

        print(
            f"L/D importance:             "
            f"{mission_weights['lift_to_drag'] * 100.0:.0f}%"
        )

        print(
            f"Stall-margin importance:    "
            f"{mission_weights['stall_margin'] * 100.0:.0f}%"
        )

        print(
            f"Wing-loading importance:    "
            f"{mission_weights['wing_loading'] * 100.0:.0f}%"
        )

        print(
            f"Aspect-ratio importance:    "
            f"{mission_weights['aspect_ratio'] * 100.0:.0f}%"
        )

    # ======================================================
    # Penalty report
    # ======================================================

    penalties = best_design.get(
        "penalties",
        {},
    )

    print("\nFEASIBILITY AND PENALTIES")
    print("-" * 72)

    if penalties:
        print(
            "The best design received the following "
            "aerodynamic penalties:"
        )

        for penalty_name, penalty_value in penalties.items():
            readable_name = penalty_name.replace(
                "_",
                " ",
            ).title()

            print(
                f"- {readable_name}: "
                f"-{penalty_value:.1f} points"
            )

    else:
        print(
            "No aerodynamic feasibility penalties "
            "were applied."
        )

    print("=" * 72)

    return best_design