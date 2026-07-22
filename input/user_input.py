from input.requirements import UserRequirements


def get_float_input(prompt, minimum=None):
    """
    Repeatedly ask the user for a numeric value until a valid value is entered.

    Parameters
    ----------
    prompt : str
        Message displayed to the user.

    minimum : float, optional
        Smallest allowed value.

    Returns
    -------
    float
        Valid numeric user input.
    """

    while True:
        try:
            value = float(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Value must be at least {minimum}.")
                continue

            return value

        except ValueError:
            print("Invalid input. Enter a numerical value.")


def get_mission_input():
    """
    Ask the user to select an aircraft mission.
    """

    missions = {
        "1": "Cargo",
        "2": "Survey",
        "3": "Trainer",
        "4": "Racing",
        "5": "VTOL Support",
    }

    print("\nAVAILABLE MISSIONS")
    print("-" * 40)

    for number, mission in missions.items():
        print(f"{number}. {mission}")

    while True:
        selection = input("\nSelect a mission number: ").strip()

        if selection in missions:
            return missions[selection]

        print("Invalid selection. Enter a number from 1 to 5.")


def collect_user_requirements():
    """
    Collect aircraft design requirements from the user.

    Returns
    -------
    UserRequirements
        Validated aircraft design requirements.
    """

    print("\n" + "=" * 72)
    print("AERODESIGNX AIRCRAFT REQUIREMENT INPUT")
    print("=" * 72)

    mission = get_mission_input()

    payload_mass = get_float_input(
        "\nPayload mass (kg): ",
        minimum=0.0,
    )

    cruise_speed = get_float_input(
        "Desired cruise speed (m/s): ",
        minimum=1.0,
    )

    max_wingspan = get_float_input(
        "Maximum wingspan (m): ",
        minimum=0.1,
    )

    battery_capacity = get_float_input(
        "Battery capacity (Wh): ",
        minimum=1.0,
    )

    requirements = UserRequirements(
        mission=mission,
        payload_mass=payload_mass,
        cruise_speed=cruise_speed,
        max_wingspan=max_wingspan,
        battery_capacity=battery_capacity,
    )

    requirements.validate()

    return requirements

if __name__ == "__main__":
    requirements = collect_user_requirements()
    requirements.display()