"""
Aircraft Mass Model

Estimates component masses for a conceptual fixed-wing UAV.
"""


def estimate_wing_mass(
    wing_area,
    aspect_ratio,
    wing_areal_density=2.5,
    aspect_ratio_penalty=0.08,
):
    """
    Estimate wing structural mass.

    Parameters
    ----------
    wing_area : float
        Wing planform area in square meters.
    aspect_ratio : float
        Wing aspect ratio.
    wing_areal_density : float
        Baseline wing mass per unit area in kg/m^2.
    aspect_ratio_penalty : float
        Additional mass penalty for slender wings.

    Returns
    -------
    float
        Estimated wing mass in kilograms.
    """

    if wing_area <= 0:
        raise ValueError("Wing area must be positive.")

    if aspect_ratio <= 0:
        raise ValueError("Aspect ratio must be positive.")

    baseline_mass = wing_area * wing_areal_density

    slenderness_factor = 1.0 + aspect_ratio_penalty * max(
        0.0,
        aspect_ratio - 4.0,
    )

    return baseline_mass * slenderness_factor


def estimate_battery_mass(
    battery_capacity_wh,
    battery_specific_energy_wh_per_kg=200.0,
):
    """
    Estimate battery mass from battery energy capacity.

    Parameters
    ----------
    battery_capacity_wh : float
        Battery capacity in watt-hours.
    battery_specific_energy_wh_per_kg : float
        Battery-level specific energy in Wh/kg.

    Returns
    -------
    float
        Estimated battery mass in kilograms.
    """

    if battery_capacity_wh < 0:
        raise ValueError("Battery capacity cannot be negative.")

    if battery_specific_energy_wh_per_kg <= 0:
        raise ValueError(
            "Battery specific energy must be positive."
        )

    return (
        battery_capacity_wh
        / battery_specific_energy_wh_per_kg
    )


def estimate_total_mass(
    wing_mass,
    battery_mass,
    fuselage_mass,
    tail_mass,
    propulsion_mass,
    avionics_mass,
    payload_mass,
):
    """
    Add aircraft component masses.

    Returns
    -------
    float
        Estimated total aircraft mass in kilograms.
    """

    component_masses = [
        wing_mass,
        battery_mass,
        fuselage_mass,
        tail_mass,
        propulsion_mass,
        avionics_mass,
        payload_mass,
    ]

    if any(mass < 0 for mass in component_masses):
        raise ValueError(
            "Aircraft component masses cannot be negative."
        )

    return sum(component_masses)