"""
Aircraft Configuration Selection

Defines the aircraft layouts available in AeroDesignX and evaluates
how well each configuration matches a selected mission.
"""


AIRCRAFT_CONFIGURATIONS = {
    "Conventional": {
        "description": (
            "Standard fuselage with a main wing and rear horizontal "
            "and vertical tail surfaces."
        ),
        "stability": 9,
        "speed": 7,
        "payload": 8,
        "efficiency": 7,
        "simplicity": 9,
    },

    "Twin Boom": {
        "description": (
            "Central fuselage or payload pod with two rear booms "
            "supporting the tail."
        ),
        "stability": 8,
        "speed": 7,
        "payload": 9,
        "efficiency": 8,
        "simplicity": 6,
    },

    "Flying Wing": {
        "description": (
            "Tailless aircraft in which most components are contained "
            "inside the wing."
        ),
        "stability": 6,
        "speed": 9,
        "payload": 6,
        "efficiency": 10,
        "simplicity": 7,
    },
}


MISSION_CONFIGURATION_WEIGHTS = {
    "Cargo": {
        "stability": 0.20,
        "speed": 0.10,
        "payload": 0.35,
        "efficiency": 0.20,
        "simplicity": 0.15,
    },

    "Survey": {
        "stability": 0.25,
        "speed": 0.10,
        "payload": 0.15,
        "efficiency": 0.35,
        "simplicity": 0.15,
    },

    "Trainer": {
        "stability": 0.35,
        "speed": 0.10,
        "payload": 0.10,
        "efficiency": 0.15,
        "simplicity": 0.30,
    },

    "Racing": {
        "stability": 0.10,
        "speed": 0.45,
        "payload": 0.05,
        "efficiency": 0.25,
        "simplicity": 0.15,
    },

    "VTOL Support": {
        "stability": 0.25,
        "speed": 0.05,
        "payload": 0.30,
        "efficiency": 0.15,
        "simplicity": 0.25,
    },
}


def score_configuration(configuration_name, mission_name):
    """
    Calculate how well an aircraft configuration matches a mission.

    Returns a score from 0 to 100.
    """
    configuration = AIRCRAFT_CONFIGURATIONS[configuration_name]
    weights = MISSION_CONFIGURATION_WEIGHTS[mission_name]

    weighted_score = (
        configuration["stability"] * weights["stability"]
        + configuration["speed"] * weights["speed"]
        + configuration["payload"] * weights["payload"]
        + configuration["efficiency"] * weights["efficiency"]
        + configuration["simplicity"] * weights["simplicity"]
    )

    return weighted_score * 10


def rank_configurations(mission_name):
    """
    Rank every aircraft configuration for the selected mission.
    """
    ranked_configurations = []

    for configuration_name in AIRCRAFT_CONFIGURATIONS:
        score = score_configuration(
            configuration_name,
            mission_name,
        )

        result = {
            "name": configuration_name,
            "score": score,
            "description": AIRCRAFT_CONFIGURATIONS[
                configuration_name
            ]["description"],
        }

        ranked_configurations.append(result)

    ranked_configurations.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return ranked_configurations


def recommend_configuration(mission_name):
    """
    Return the highest-ranked configuration for the mission.
    """
    ranked_configurations = rank_configurations(mission_name)
    return ranked_configurations[0]


def print_configuration_comparison(mission_name):
    """
    Print the ranked aircraft-configuration comparison.
    """
    ranked_configurations = rank_configurations(mission_name)
    recommended = ranked_configurations[0]

    print("\n" + "=" * 72)
    print("AERODESIGNX AIRCRAFT CONFIGURATION RECOMMENDATION")
    print("=" * 72)

    print(f"Mission:                   {mission_name}")
    print(f"Recommended Configuration: {recommended['name']}")
    print(f"Configuration Score:       {recommended['score']:.1f}/100")
    print(f"Description:               {recommended['description']}")

    print("\nCONFIGURATION COMPARISON")
    print("-" * 72)
    print(f"{'Rank':<8}{'Configuration':<22}{'Score':<12}")
    print("-" * 72)

    for rank, configuration in enumerate(
        ranked_configurations,
        start=1,
    ):
        print(
            f"{rank:<8}"
            f"{configuration['name']:<22}"
            f"{configuration['score']:.1f}/100"
        )

    print("=" * 72)