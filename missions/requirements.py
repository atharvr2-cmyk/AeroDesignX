"""
Mission Requirements

Converts a mission profile into measurable aircraft design requirements.
"""


def calculate_mission_requirements(
    mission,
    base_aircraft_mass=3.0,
    gravity=9.81,
    reserve_fraction=0.20,
):
    """
    Convert a mission into engineering requirements.

    Parameters
    ----------
    mission : Mission
        Mission profile containing speed, endurance, range, payload,
        and stall-speed requirements.

    base_aircraft_mass : float
        Estimated aircraft mass without payload, in kilograms.

    gravity : float
        Gravitational acceleration in meters per second squared.

    reserve_fraction : float
        Additional endurance reserve expressed as a decimal.

    Returns
    -------
    dict
        Dictionary containing calculated mission requirements.
    """

    total_mass = base_aircraft_mass + mission.payload_mass
    required_lift = total_mass * gravity

    endurance_with_reserve = (
        mission.endurance_hours * (1.0 + reserve_fraction)
    )

    cruise_distance_km = (
        mission.cruise_speed
        * mission.endurance_hours
        * 3600.0
        / 1000.0
    )

    required_range_km = max(
        mission.range_km,
        cruise_distance_km,
    )

    return {
        "mission_name": mission.name,
        "base_aircraft_mass": base_aircraft_mass,
        "payload_mass": mission.payload_mass,
        "total_mass": total_mass,
        "required_lift": required_lift,
        "cruise_speed": mission.cruise_speed,
        "maximum_stall_speed": mission.max_stall_speed,
        "required_endurance_hours": mission.endurance_hours,
        "endurance_with_reserve_hours": endurance_with_reserve,
        "stated_range_km": mission.range_km,
        "cruise_distance_km": cruise_distance_km,
        "required_range_km": required_range_km,
        "reserve_fraction": reserve_fraction,
    }


def display_mission_requirements(requirements):
    """
    Print calculated mission requirements.

    Parameters
    ----------
    requirements : dict
        Dictionary returned by calculate_mission_requirements().
    """

    print()
    print("=" * 72)
    print("CALCULATED MISSION REQUIREMENTS")
    print("=" * 72)

    print(f"Mission:                  {requirements['mission_name']}")
    print(
        f"Base Aircraft Mass:       "
        f"{requirements['base_aircraft_mass']:.2f} kg"
    )
    print(
        f"Payload Mass:             "
        f"{requirements['payload_mass']:.2f} kg"
    )
    print(
        f"Estimated Total Mass:     "
        f"{requirements['total_mass']:.2f} kg"
    )
    print(
        f"Required Lift:            "
        f"{requirements['required_lift']:.2f} N"
    )
    print(
        f"Cruise Speed:             "
        f"{requirements['cruise_speed']:.1f} m/s"
    )
    print(
        f"Maximum Stall Speed:      "
        f"{requirements['maximum_stall_speed']:.1f} m/s"
    )
    print(
        f"Required Endurance:       "
        f"{requirements['required_endurance_hours']:.2f} hr"
    )
    print(
        f"Endurance with Reserve:   "
        f"{requirements['endurance_with_reserve_hours']:.2f} hr"
    )
    print(
        f"Mission-Stated Range:     "
        f"{requirements['stated_range_km']:.1f} km"
    )
    print(
        f"Distance at Cruise:       "
        f"{requirements['cruise_distance_km']:.1f} km"
    )
    print(
        f"Required Design Range:    "
        f"{requirements['required_range_km']:.1f} km"
    )

    print("=" * 72)