"""
Mission Definition

Defines the mission requirements that an aircraft design must satisfy.
"""


class Mission:
    """
    Represents the operating mission for an aircraft.

    A mission stores the performance targets that will later be used
    to evaluate and optimize aircraft designs.
    """

    def __init__(
        self,
        name,
        description,
        cruise_speed,
        endurance_hours,
        range_km,
        payload_mass,
        max_stall_speed,
    ):
        """
        Initialize a mission.

        Parameters
        ----------
        name : str
            Name of the mission.

        description : str
            Short explanation of the mission.

        cruise_speed : float
            Required cruise speed in meters per second.

        endurance_hours : float
            Required flight endurance in hours.

        range_km : float
            Required mission range in kilometers.

        payload_mass : float
            Required payload mass in kilograms.

        max_stall_speed : float
            Maximum acceptable stall speed in meters per second.
        """

        self.name = name
        self.description = description
        self.cruise_speed = cruise_speed
        self.endurance_hours = endurance_hours
        self.range_km = range_km
        self.payload_mass = payload_mass
        self.max_stall_speed = max_stall_speed

    def display(self):
        """
        Print the mission requirements.
        """

        print()
        print("=" * 72)
        print(f"MISSION PROFILE: {self.name.upper()}")
        print("=" * 72)

        print(f"Description:        {self.description}")
        print(f"Cruise Speed:       {self.cruise_speed:.1f} m/s")
        print(f"Endurance:          {self.endurance_hours:.1f} hr")
        print(f"Range:              {self.range_km:.1f} km")
        print(f"Payload Mass:       {self.payload_mass:.2f} kg")
        print(f"Maximum Stall Speed:{self.max_stall_speed:>8.1f} m/s")

        print("=" * 72)

    def to_dict(self):
        """
        Return the mission information as a dictionary.

        This will make the mission easy to use with the existing
        dictionary-based AeroDesignX optimization system.
        """

        return {
            "name": self.name,
            "description": self.description,
            "cruise_speed": self.cruise_speed,
            "endurance_hours": self.endurance_hours,
            "range_km": self.range_km,
            "payload_mass": self.payload_mass,
            "max_stall_speed": self.max_stall_speed,
        }