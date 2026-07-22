"""
Mission profiles used throughout AeroDesignX.

Each mission defines the performance requirements
that the optimizer attempts to satisfy.
"""

MISSION_DATABASE = {

    "Trainer": {
        "description": "General purpose trainer aircraft",
        "payload_kg": 0.5,
        "range_km": 10,
        "endurance_hr": 0.75,
        "cruise_speed": 15,
        "stall_speed": 10,
        "priority": "Balanced"
    },

    "Cargo": {
        "description": "Payload transport UAV",
        "payload_kg": 2.0,
        "range_km": 15,
        "endurance_hr": 1.5,
        "cruise_speed": 18,
        "stall_speed": 11,
        "priority": "Payload"
    },

    "Survey": {
        "description": "Long endurance mapping aircraft",
        "payload_kg": 1.0,
        "range_km": 40,
        "endurance_hr": 3.0,
        "cruise_speed": 16,
        "stall_speed": 9,
        "priority": "Endurance"
    },

    "Racing": {
        "description": "High-speed racing UAV",
        "payload_kg": 0.2,
        "range_km": 5,
        "endurance_hr": 0.30,
        "cruise_speed": 35,
        "stall_speed": 18,
        "priority": "Speed"
    },

    "VTOL Support": {
        "description": "Support aircraft for VTOL missions",
        "payload_kg": 1.5,
        "range_km": 20,
        "endurance_hr": 1.25,
        "cruise_speed": 20,
        "stall_speed": 10,
        "priority": "Versatility"
    }

}

def get_mission_profile(mission_name):
    """
    Return the requirements for a selected mission.

    Parameters
    ----------
    mission_name : str
        Name of the mission profile.

    Returns
    -------
    dict
        Copy of the selected mission requirements.

    Raises
    ------
    ValueError
        If the mission name does not exist.
    """

    if mission_name not in MISSION_DATABASE:
        available_missions = ", ".join(MISSION_DATABASE.keys())

        raise ValueError(
            f"Unknown mission profile: {mission_name}. "
            f"Available missions: {available_missions}"
        )

    mission = MISSION_DATABASE[mission_name].copy()
    mission["mission_name"] = mission_name

    return mission


def list_mission_profiles():
    """
    Return a list of all available mission-profile names.
    """

    return list(MISSION_DATABASE.keys())


def print_mission_profile(mission_name):
    """
    Print a formatted summary of a mission profile.
    """

    mission = get_mission_profile(mission_name)

    print("\n" + "=" * 72)
    print("AERODESIGNX MISSION REQUIREMENTS")
    print("=" * 72)

    print(f"Mission:            {mission_name}")
    print(f"Description:        {mission['description']}")
    print(f"Payload:            {mission['payload_kg']:.2f} kg")
    print(f"Required Range:     {mission['range_km']:.1f} km")
    print(f"Required Endurance: {mission['endurance_hr']:.2f} hr")
    print(f"Cruise Speed:       {mission['cruise_speed']:.1f} m/s")
    print(f"Maximum Stall Speed:{mission['stall_speed']:.1f} m/s")
    print(f"Design Priority:    {mission['priority']}")

    print("=" * 72)