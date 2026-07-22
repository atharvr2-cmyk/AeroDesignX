"""
Mission recommendation tools for AeroDesignX.

Uses user-defined aircraft requirements to recommend the
closest available mission profile.
"""

from requirements.mission_profiles import MISSION_DATABASE


def recommend_mission(
    payload_kg,
    range_km,
    endurance_hr,
    cruise_speed,
):
    """
    Recommend the mission profile that most closely matches
    the user's aircraft requirements.

    Parameters
    ----------
    payload_kg : float
        Required payload mass in kilograms.

    range_km : float
        Required aircraft range in kilometers.

    endurance_hr : float
        Required endurance in hours.

    cruise_speed : float
        Desired cruise speed in meters per second.

    Returns
    -------
    dict
        Recommended mission name, profile, score, and comparison data.
    """

    user_requirements = {
        "payload_kg": payload_kg,
        "range_km": range_km,
        "endurance_hr": endurance_hr,
        "cruise_speed": cruise_speed,
    }

    comparison_results = []

    for mission_name, mission_profile in MISSION_DATABASE.items():
        total_difference = 0.0
        category_differences = {}

        for requirement_name, user_value in user_requirements.items():
            mission_value = mission_profile[requirement_name]

            scale = max(abs(mission_value), 1.0)

            normalized_difference = (
                abs(user_value - mission_value) / scale
            )

            category_differences[requirement_name] = (
                normalized_difference
            )

            total_difference += normalized_difference

        average_difference = (
            total_difference / len(user_requirements)
        )

        match_score = max(
            0.0,
            100.0 * (1.0 - average_difference),
        )

        comparison_results.append(
            {
                "mission_name": mission_name,
                "match_score": match_score,
                "average_difference": average_difference,
                "category_differences": category_differences,
            }
        )

    comparison_results.sort(
        key=lambda result: result["average_difference"]
    )

    best_match = comparison_results[0]
    recommended_name = best_match["mission_name"]

    recommended_profile = MISSION_DATABASE[
        recommended_name
    ].copy()

    recommended_profile["mission_name"] = recommended_name

    return {
        "recommended_mission": recommended_name,
        "match_score": best_match["match_score"],
        "mission_profile": recommended_profile,
        "comparison_results": comparison_results,
        "user_requirements": user_requirements,
    }


def print_mission_recommendation(recommendation):
    """
    Print a formatted mission recommendation report.
    """

    print()
    print("=" * 72)
    print("AERODESIGNX MISSION RECOMMENDATION")
    print("=" * 72)

    print(
        f"Recommended Mission: "
        f"{recommendation['recommended_mission']}"
    )

    print(
        f"Match Score:         "
        f"{recommendation['match_score']:.1f}/100"
    )

    profile = recommendation["mission_profile"]

    print(
        f"Description:         "
        f"{profile['description']}"
    )

    print(
        f"Design Priority:     "
        f"{profile['priority']}"
    )

    print()
    print("MISSION COMPARISON")
    print("-" * 72)

    print(
        f"{'Mission':<18}"
        f"{'Match Score':<16}"
    )

    print("-" * 34)

    for result in recommendation["comparison_results"]:
        print(
            f"{result['mission_name']:<18}"
            f"{result['match_score']:<16.1f}"
        )

    print("=" * 72)