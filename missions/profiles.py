"""
Mission Profiles

Provides predefined missions for common UAV applications.
"""

from missions.mission import Mission


def surveillance_mission():
    """
    Long-endurance mission for observation and monitoring.
    """

    return Mission(
        name="Surveillance UAV",
        description="Long-endurance aerial observation and monitoring.",
        cruise_speed=15.0,
        endurance_hours=2.0,
        range_km=40.0,
        payload_mass=0.50,
        max_stall_speed=10.0,
    )


def mapping_mission():
    """
    Mission for aerial photography, surveying, and mapping.
    """

    return Mission(
        name="Mapping UAV",
        description="Aerial surveying and high-resolution terrain mapping.",
        cruise_speed=18.0,
        endurance_hours=1.5,
        range_km=30.0,
        payload_mass=0.75,
        max_stall_speed=11.0,
    )


def cargo_mission():
    """
    Mission focused on carrying a relatively heavy payload.
    """

    return Mission(
        name="Cargo UAV",
        description="Short-range transport of a heavy payload.",
        cruise_speed=16.0,
        endurance_hours=1.0,
        range_km=20.0,
        payload_mass=2.00,
        max_stall_speed=12.0,
    )


def trainer_mission():
    """
    Stable and forgiving mission for training or general-purpose flight.
    """

    return Mission(
        name="Trainer UAV",
        description="Stable, predictable aircraft for training and testing.",
        cruise_speed=14.0,
        endurance_hours=1.0,
        range_km=15.0,
        payload_mass=0.25,
        max_stall_speed=9.0,
    )


def racing_mission():
    """
    High-speed mission where endurance and payload are less important.
    """

    return Mission(
        name="Racing UAV",
        description="High-speed aircraft optimized for short-duration flight.",
        cruise_speed=30.0,
        endurance_hours=0.25,
        range_km=8.0,
        payload_mass=0.10,
        max_stall_speed=15.0,
    )


def get_all_missions():
    """
    Return all predefined mission profiles.

    Returns
    -------
    dict
        Dictionary containing each mission profile.
    """

    return {
        "surveillance": surveillance_mission(),
        "mapping": mapping_mission(),
        "cargo": cargo_mission(),
        "trainer": trainer_mission(),
        "racing": racing_mission(),
    }


def get_mission(mission_name):
    """
    Return a predefined mission using its name.

    Parameters
    ----------
    mission_name : str
        Mission key such as 'surveillance', 'mapping', or 'cargo'.

    Returns
    -------
    Mission
        Selected mission object.

    Raises
    ------
    ValueError
        If the requested mission does not exist.
    """

    missions = get_all_missions()
    mission_key = mission_name.lower().strip()

    if mission_key not in missions:
        available = ", ".join(missions.keys())

        raise ValueError(
            f"Unknown mission '{mission_name}'. "
            f"Available missions: {available}"
        )

    return missions[mission_key]