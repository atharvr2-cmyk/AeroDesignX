"""
Aircraft Concept Generator

Converts high-level aircraft concepts into complete
Aircraft and Wing objects for analysis.
"""

from aircraft.assembly import Aircraft
from geometry.wing import Wing
from design.concepts import ALL_CONCEPTS


def generate_aircraft_from_concept(
    concept,
    mass=3.0,
    gravity=9.81,
    air_density=1.225,
    airfoil="4412",
    taper_ratio=0.65,
    sweep=0.0,
    dihedral=3.0
):
    """
    Generate a complete aircraft from a predefined concept.

    Parameters
    ----------
    concept : AircraftConcept
        High-level aircraft configuration.

    mass : float
        Aircraft mass in kilograms.

    gravity : float
        Gravitational acceleration in m/s^2.

    air_density : float
        Atmospheric air density in kg/m^3.

    airfoil : str
        NACA four-digit airfoil designation.

    taper_ratio : float
        Ratio of tip chord to root chord.

    sweep : float
        Wing sweep angle in degrees.

    dihedral : float
        Wing dihedral angle in degrees.

    Returns
    -------
    Aircraft
        Fully generated aircraft model.
    """

    if mass <= 0:
        raise ValueError("Aircraft mass must be greater than zero.")

    if gravity <= 0:
        raise ValueError("Gravity must be greater than zero.")

    if air_density <= 0:
        raise ValueError("Air density must be greater than zero.")

    if not 0 < taper_ratio <= 1:
        raise ValueError(
            "Taper ratio must be greater than zero and no greater than one."
        )

    # Aspect ratio relationship:
    # AR = span^2 / area
    #
    # Rearranged:
    # area = span^2 / AR
    wing_area = concept.span ** 2 / concept.aspect_ratio

    # For a trapezoidal wing:
    # area = span / 2 * (root chord + tip chord)
    #
    # Since tip chord = taper ratio * root chord:
    # root chord = 2 * area / (span * (1 + taper ratio))
    root_chord = (
        2 * wing_area
        / (concept.span * (1 + taper_ratio))
    )

    tip_chord = taper_ratio * root_chord

    wing = Wing(
        span=concept.span,
        root_chord=root_chord,
        tip_chord=tip_chord,
        airfoil=airfoil,
        dihedral=dihedral,
        sweep=sweep
    )

    aircraft = Aircraft(
        name=concept.name,
        mass=mass,
        gravity=gravity,
        cruise_speed=concept.cruise_speed,
        air_density=air_density,
        wing=wing,
        airfoil=airfoil
    )

    aircraft.description = concept.description

    return aircraft


def generate_all_concepts(
    mass=3.0,
    gravity=9.81,
    air_density=1.225,
    airfoil="4412",
    taper_ratio=0.65,
    sweep=0.0,
    dihedral=3.0
):
    """
    Generate aircraft models for every predefined concept.

    Returns
    -------
    list
        List containing one Aircraft object for each concept.
    """

    aircraft_list = []

    for concept in ALL_CONCEPTS:
        aircraft = generate_aircraft_from_concept(
            concept=concept,
            mass=mass,
            gravity=gravity,
            air_density=air_density,
            airfoil=airfoil,
            taper_ratio=taper_ratio,
            sweep=sweep,
            dihedral=dihedral
        )

        aircraft_list.append(aircraft)

    return aircraft_list


def display_generated_concepts(aircraft_list):
    """
    Print the geometry of every generated aircraft concept.
    """

    print("=" * 76)
    print("GENERATED AIRCRAFT CONCEPTS")
    print("=" * 76)

    for aircraft in aircraft_list:
        wing = aircraft.wing

        print(f"\nAircraft:       {aircraft.name}")
        print(f"Description:    {aircraft.description}")
        print(f"Mass:           {aircraft.mass:.2f} kg")
        print(f"Span:           {wing.span:.2f} m")
        print(f"Root Chord:     {wing.root_chord:.3f} m")
        print(f"Tip Chord:      {wing.tip_chord:.3f} m")
        print(f"Wing Area:      {wing.area:.3f} m^2")
        print(f"Aspect Ratio:   {wing.aspect_ratio():.2f}")
        print(f"Taper Ratio:    {wing.taper_ratio:.2f}")
        print(
            f"Mean Aero Chord:{wing.mean_aerodynamic_chord():.3f} m"
        )
        print(f"Cruise Speed:   {aircraft.cruise_speed:.1f} m/s")
        print(f"Airfoil:        NACA {wing.airfoil}")
        print("-" * 76)


if __name__ == "__main__":
    generated_aircraft = generate_all_concepts()

    display_generated_concepts(generated_aircraft)