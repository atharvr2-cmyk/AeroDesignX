"""
Aircraft Concept Evaluator

Analyzes, scores, ranks, and compares all generated
aircraft concepts.
"""

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
from analysis.parameter_sweep import score_sweep_result
from design.generator import generate_all_concepts
from analysis.parameter_sweep import score_sweep_result
from visualization.plot_concepts import plot_concept_comparison


def evaluate_aircraft(aircraft, cl_max=1.5):
    """
    Evaluate the aerodynamic performance of one aircraft.

    Parameters
    ----------
    aircraft : Aircraft
        Aircraft object to evaluate.

    cl_max : float
        Maximum lift coefficient used for stall-speed estimation.

    Returns
    -------
    dict
        Calculated aircraft performance values.
    """

    weight = aircraft.mass * aircraft.gravity
    wing_area = aircraft.wing.area
    aspect_ratio = aircraft.wing.aspect_ratio()

    cl_required = required_cl(
        mass=aircraft.mass,
        gravity=aircraft.gravity,
        air_density=aircraft.air_density,
        velocity=aircraft.cruise_speed,
        wing_area=wing_area,
    )

    cd_total = total_drag_coefficient(
        cl=cl_required,
        aspect_ratio=aspect_ratio,
    )

    drag = drag_force(
        air_density=aircraft.air_density,
        velocity=aircraft.cruise_speed,
        wing_area=wing_area,
        cd=cd_total,
    )

    lift_drag = lift_to_drag_ratio(
        lift=weight,
        drag=drag,
    )

    stall_speed_value = stall_speed(
        weight=weight,
        air_density=aircraft.air_density,
        wing_area=wing_area,
        cl_max=cl_max,
    )

    wing_loading_value = wing_loading(
        weight=weight,
        wing_area=wing_area,
    )

    result = {
        "name": aircraft.name,
        "description": aircraft.description,
        "aircraft": aircraft,
        "span": aircraft.wing.span,
        "wing_area": wing_area,
        "aspect_ratio": aspect_ratio,
        "cruise_speed": aircraft.cruise_speed,
        "required_cl": cl_required,
        "total_cd": cd_total,
        "drag": drag,
        "lift_to_drag": lift_drag,
        "stall_speed": stall_speed_value,
        "wing_loading": wing_loading_value,
    }

    result["score"] = score_sweep_result(result)

    return result


def evaluate_all_concepts(aircraft_list, cl_max=1.5):
    """
    Evaluate every aircraft in a supplied list.
    """

    results = []

    for aircraft in aircraft_list:
        result = evaluate_aircraft(
            aircraft=aircraft,
            cl_max=cl_max,
        )

        results.append(result)

    return results


def rank_concepts(results):
    """
    Rank concepts from highest score to lowest score.

    Lift-to-drag ratio is used as a secondary ranking
    criterion when two aircraft have the same score.
    """

    return sorted(
        results,
        key=lambda result: (
            result["score"],
            result["lift_to_drag"],
        ),
        reverse=True,
    )


def display_ranked_results(ranked_results):
    """
    Print a comparison table of all evaluated concepts.
    """

    print("\n" + "=" * 112)
    print("AIRCRAFT CONCEPT COMPARISON")
    print("=" * 112)

    print(
        f"{'Rank':<6}"
        f"{'Concept':<16}"
        f"{'Span':<9}"
        f"{'Area':<10}"
        f"{'AR':<8}"
        f"{'CL Req.':<11}"
        f"{'Drag':<11}"
        f"{'L/D':<10}"
        f"{'Stall V':<11}"
        f"{'W/S':<11}"
        f"{'Score':<8}"
    )

    print("-" * 112)

    for rank, result in enumerate(ranked_results, start=1):
        print(
            f"{rank:<6}"
            f"{result['name']:<16}"
            f"{result['span']:<9.2f}"
            f"{result['wing_area']:<10.3f}"
            f"{result['aspect_ratio']:<8.2f}"
            f"{result['required_cl']:<11.3f}"
            f"{result['drag']:<11.2f}"
            f"{result['lift_to_drag']:<10.2f}"
            f"{result['stall_speed']:<11.2f}"
            f"{result['wing_loading']:<11.2f}"
            f"{result['score']:<8}"
        )

    print("=" * 112)


def display_best_design(ranked_results):
    """
    Print the highest-ranked aircraft concept.
    """

    if not ranked_results:
        print("No aircraft concepts were evaluated.")
        return

    best = ranked_results[0]

    print("\n" + "=" * 62)
    print("RECOMMENDED AIRCRAFT CONCEPT")
    print("=" * 62)

    print(f"Concept:           {best['name']}")
    print(f"Description:       {best['description']}")
    print(f"Overall Score:     {best['score']}/100")
    print(f"Lift-to-Drag:      {best['lift_to_drag']:.2f}")
    print(f"Required CL:       {best['required_cl']:.3f}")
    print(f"Drag:              {best['drag']:.2f} N")
    print(f"Stall Speed:       {best['stall_speed']:.2f} m/s")
    print(f"Wing Loading:      {best['wing_loading']:.2f} N/m^2")
    print(f"Aspect Ratio:      {best['aspect_ratio']:.2f}")

    print("\nSelection Reason:")

    print(
        f"{best['name']} achieved the highest combined design "
        "score based on aerodynamic efficiency, lift requirement, "
        "stall performance, and wing loading."
    )

    print("=" * 62)


if __name__ == "__main__":
    aircraft_list = generate_all_concepts()

    results = evaluate_all_concepts(
        aircraft_list=aircraft_list,
        cl_max=1.5,
    )

    ranked_results = rank_concepts(results)

    display_ranked_results(ranked_results)
    display_best_design(ranked_results)
    plot_concept_comparison(ranked_results)