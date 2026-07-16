"""
Mission and Battery Sizing

Calculates cruise power, required battery energy,
battery mass, and converged aircraft mass.
"""

from aerodynamics.drag import (
    drag_force,
    total_drag_coefficient,
)
from aerodynamics.lift import required_cl
from aerodynamics.performance import stall_speed
from analysis.mass_model import (
    estimate_battery_mass,
    estimate_total_mass,
    estimate_wing_mass,
)


def required_electrical_power(
    drag,
    cruise_speed,
    propulsive_efficiency=0.70,
    avionics_power_w=15.0,
):
    """
    Estimate total electrical power required in cruise.

    Mechanical propulsive power is drag multiplied by speed.
    Electrical power is higher because the propulsion system
    is not perfectly efficient.
    """

    if drag < 0:
        raise ValueError("Drag cannot be negative.")

    if cruise_speed <= 0:
        raise ValueError("Cruise speed must be positive.")

    if not 0 < propulsive_efficiency <= 1:
        raise ValueError(
            "Propulsive efficiency must be between 0 and 1."
        )

    propulsive_power = drag * cruise_speed

    electrical_propulsion_power = (
        propulsive_power / propulsive_efficiency
    )

    return (
        electrical_propulsion_power
        + avionics_power_w
    )


def required_battery_capacity(
    average_power_w,
    endurance_hours,
    usable_fraction=0.80,
    reserve_fraction=0.15,
):
    """
    Calculate installed battery capacity for a mission.

    Parameters
    ----------
    average_power_w : float
        Average electrical power required.
    endurance_hours : float
        Required mission endurance.
    usable_fraction : float
        Fraction of battery capacity that may be used.
    reserve_fraction : float
        Additional mission-energy reserve.

    Returns
    -------
    float
        Required installed capacity in watt-hours.
    """

    if average_power_w <= 0:
        raise ValueError(
            "Average power must be positive."
        )

    if endurance_hours <= 0:
        raise ValueError(
            "Endurance must be positive."
        )

    if not 0 < usable_fraction <= 1:
        raise ValueError(
            "Usable fraction must be between 0 and 1."
        )

    if reserve_fraction < 0:
        raise ValueError(
            "Reserve fraction cannot be negative."
        )

    mission_energy_wh = (
        average_power_w * endurance_hours
    )

    energy_with_reserve = mission_energy_wh * (
        1.0 + reserve_fraction
    )

    return energy_with_reserve / usable_fraction

def size_aircraft_for_mission(
    wing,
    initial_mass,
    gravity,
    air_density,
    cruise_speed,
    cl_max,
    endurance_hours,
    fuselage_mass,
    tail_mass,
    propulsion_mass,
    avionics_mass,
    payload_mass,
    battery_specific_energy_wh_per_kg=200.0,
    propulsive_efficiency=0.70,
    avionics_power_w=15.0,
    battery_usable_fraction=0.80,
    reserve_fraction=0.15,
    mass_tolerance=0.001,
    max_iterations=100,
):
    """
    Iteratively estimate aircraft mass and battery size.

    The battery changes aircraft mass. The new mass changes
    lift, drag, power, and battery requirements, so the
    calculation repeats until the mass converges.
    """

    mass = initial_mass

    wing_area = wing.area
    aspect_ratio = wing.aspect_ratio()

    wing_mass = estimate_wing_mass(
        wing_area=wing_area,
        aspect_ratio=aspect_ratio,
    )

    for iteration in range(1, max_iterations + 1):
        weight = mass * gravity

        required_cl_value = required_cl(
            mass=mass,
            gravity=gravity,
            air_density=air_density,
            velocity=cruise_speed,
            wing_area=wing_area,
        )

        total_cd_value = total_drag_coefficient(
            cl=required_cl_value,
            aspect_ratio=aspect_ratio,
        )

        drag_value = drag_force(
            air_density=air_density,
            velocity=cruise_speed,
            wing_area=wing_area,
            cd=total_cd_value,
        )

        electrical_power_w = required_electrical_power(
            drag=drag_value,
            cruise_speed=cruise_speed,
            propulsive_efficiency=propulsive_efficiency,
            avionics_power_w=avionics_power_w,
        )

        battery_capacity_wh = required_battery_capacity(
            average_power_w=electrical_power_w,
            endurance_hours=endurance_hours,
            usable_fraction=battery_usable_fraction,
            reserve_fraction=reserve_fraction,
        )

        battery_mass = estimate_battery_mass(
            battery_capacity_wh=battery_capacity_wh,
            battery_specific_energy_wh_per_kg=(
                battery_specific_energy_wh_per_kg
            ),
        )

        updated_mass = estimate_total_mass(
            wing_mass=wing_mass,
            battery_mass=battery_mass,
            fuselage_mass=fuselage_mass,
            tail_mass=tail_mass,
            propulsion_mass=propulsion_mass,
            avionics_mass=avionics_mass,
            payload_mass=payload_mass,
        )

        mass_change = abs(updated_mass - mass)

        mass = updated_mass

        if mass_change < mass_tolerance:
            break

    stall_speed_value = stall_speed(
        weight=mass * gravity,
        air_density=air_density,
        wing_area=wing_area,
        cl_max=cl_max,
    )

    converged = mass_change < mass_tolerance

    return {
        "total_mass": mass,
        "wing_mass": wing_mass,
        "battery_mass": battery_mass,
        "battery_capacity_wh": battery_capacity_wh,
        "required_cl": required_cl_value,
        "total_cd": total_cd_value,
        "drag": drag_value,
        "electrical_power_w": electrical_power_w,
        "stall_speed": stall_speed_value,
        "iterations": iteration,
        "converged": converged,
    }