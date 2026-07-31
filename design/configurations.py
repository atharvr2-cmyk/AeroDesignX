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

# Mission-specific suitability captures layout advantages that the five
# general capability ratings cannot express.  Examples include the Twin
# Boom's unobstructed payload view and rear-propeller clearance.
MISSION_LAYOUT_FIT = {
    "Cargo": {
        "Conventional": 9.0,
        "Twin Boom": 8.5,
        "Flying Wing": 5.5,
    },
    "Survey": {
        "Conventional": 7.5,
        "Twin Boom": 10.0,
        "Flying Wing": 8.5,
    },
    "Trainer": {
        "Conventional": 10.0,
        "Twin Boom": 7.5,
        "Flying Wing": 5.5,
    },
    "Racing": {
        "Conventional": 6.5,
        "Twin Boom": 6.0,
        "Flying Wing": 10.0,
    },
    "VTOL Support": {
        "Conventional": 7.0,
        "Twin Boom": 10.0,
        "Flying Wing": 4.5,
    },
}


def score_configuration(
    configuration_name,
    mission_name,
    payload_mass=0.0,
    cruise_speed=15.0,
    max_wingspan=2.0,
    battery_capacity=500.0,
):
    """
    Calculate how well an aircraft configuration matches a mission.

    Returns a score from 0 to 100.
    """
    configuration = AIRCRAFT_CONFIGURATIONS[configuration_name]
    weights = MISSION_CONFIGURATION_WEIGHTS[mission_name]

    capability_score = (
        configuration["stability"] * weights["stability"]
        + configuration["speed"] * weights["speed"]
        + configuration["payload"] * weights["payload"]
        + configuration["efficiency"] * weights["efficiency"]
        + configuration["simplicity"] * weights["simplicity"]
    )

    mission_fit = MISSION_LAYOUT_FIT[mission_name][configuration_name]

    # Mission fit is the primary selector. General capabilities prevent
    # the recommendation from being based on a mission label alone.
    score = 0.65 * mission_fit + 0.35 * capability_score

    # Requirement adjustments are deliberately small: they distinguish
    # close candidates without overpowering the selected mission.
    if payload_mass >= 2.0:
        if configuration_name == "Twin Boom":
            score += 0.45
        elif configuration_name == "Conventional":
            score += 0.25
        else:
            score -= 0.45
    elif payload_mass >= 0.75:
        if configuration_name == "Twin Boom":
            score += 0.20
        elif configuration_name == "Flying Wing":
            score -= 0.15

    if cruise_speed >= 22.0:
        if configuration_name == "Flying Wing":
            score += 0.40
        elif configuration_name == "Twin Boom":
            score -= 0.15

    if max_wingspan <= 1.2:
        if configuration_name == "Flying Wing":
            score += 0.20
        elif configuration_name == "Twin Boom":
            score -= 0.20

    if battery_capacity >= 650.0:
        if configuration_name == "Twin Boom":
            score += 0.15
        elif configuration_name == "Flying Wing":
            score += 0.10

    return max(0.0, min(100.0, score * 10.0))


def rank_configurations(
    mission_name,
    payload_mass=0.0,
    cruise_speed=15.0,
    max_wingspan=2.0,
    battery_capacity=500.0,
):
    """
    Rank every aircraft configuration for the selected mission.
    """
    ranked_configurations = []

    for configuration_name in AIRCRAFT_CONFIGURATIONS:
        score = score_configuration(
            configuration_name,
            mission_name,
            payload_mass,
            cruise_speed,
            max_wingspan,
            battery_capacity,
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


def recommend_configuration(
    mission_name,
    payload_mass=0.0,
    cruise_speed=15.0,
    max_wingspan=2.0,
    battery_capacity=500.0,
):
    """
    Return the highest-ranked configuration for the mission.
    """
    ranked_configurations = rank_configurations(
        mission_name,
        payload_mass,
        cruise_speed,
        max_wingspan,
        battery_capacity,
    )
    return ranked_configurations[0]


def print_configuration_comparison(
    mission_name,
    payload_mass=0.0,
    cruise_speed=15.0,
    max_wingspan=2.0,
    battery_capacity=500.0,
):
    """
    Print the ranked aircraft-configuration comparison.
    """
    ranked_configurations = rank_configurations(
        mission_name,
        payload_mass,
        cruise_speed,
        max_wingspan,
        battery_capacity,
    )
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