from dataclasses import dataclass


@dataclass
class UserRequirements:
    """
    Stores the aircraft design requirements provided by the user.

    This class keeps all user inputs together so they can be passed
    cleanly into the mission evaluator, optimizer, and future website.
    """

    mission: str
    payload_mass: float
    cruise_speed: float
    max_wingspan: float
    battery_capacity: float

    def validate(self):
        """
        Check whether the entered requirements are physically reasonable.

        Raises
        ------
        ValueError
            If one or more requirements are invalid.
        """

        valid_missions = {
            "cargo",
            "survey",
            "trainer",
            "racing",
            "vtol support",
        }

        if self.mission.lower() not in valid_missions:
            raise ValueError(
                f"Invalid mission '{self.mission}'. "
                f"Choose from: {', '.join(sorted(valid_missions))}."
            )

        if self.payload_mass < 0:
            raise ValueError("Payload mass cannot be negative.")

        if self.cruise_speed <= 0:
            raise ValueError("Cruise speed must be greater than zero.")

        if self.max_wingspan <= 0:
            raise ValueError("Maximum wingspan must be greater than zero.")

        if self.battery_capacity <= 0:
            raise ValueError("Battery capacity must be greater than zero.")

    def display(self):
        """
        Print the user's aircraft design requirements.
        """

        print("\n" + "=" * 72)
        print("USER DESIGN REQUIREMENTS")
        print("=" * 72)
        print(f"Mission:             {self.mission.title()}")
        print(f"Payload Mass:        {self.payload_mass:.2f} kg")
        print(f"Cruise Speed:        {self.cruise_speed:.2f} m/s")
        print(f"Maximum Wingspan:    {self.max_wingspan:.2f} m")
        print(f"Battery Capacity:    {self.battery_capacity:.1f} Wh")
        print("=" * 72)