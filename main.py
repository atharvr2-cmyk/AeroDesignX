"""
AeroDesignX Main Program

Generates the UAV wing and airfoil geometry, calculates aerodynamic
performance, prints a performance report, and displays visualization plots.
"""

from airfoils.naca import NACA4Airfoil
from aerodynamics.drag import (
    drag_force,
    induced_drag_coefficient,
    total_drag_coefficient,
)
from aerodynamics.lift import required_cl, required_lift
from aerodynamics.performance import (
    estimate_endurance,
    estimate_range,
    lift_to_drag_ratio,
    stall_speed,
    stall_speed_margin,
    wing_loading,
)
from aerodynamics.reynolds import reynolds_number
from config.parameters import (
    AIR_DENSITY,
    AIRCRAFT_NAME,
    AIRFOIL,
    CL_MAX,
    CRUISE_SPEED,
    DIHEDRAL,
    GRAVITY,
    MASS,
    ROOT_CHORD,
    SWEEP,
    TIP_CHORD,
    WING_SPAN,
    AVERAGE_POWER_W,
    BATTERY_CAPACITY_WH,
    BATTERY_USABLE_FRACTION,
)
from geometry.wing import Wing
from visualization.performance_report import print_performance_report
from visualization.plot_airfoil import plot_airfoil
from visualization.plot_drag_polar import plot_drag_polar
from visualization.plot_lift_curve import plot_lift_curve
from visualization.plot_performance import plot_performance_curves
from visualization.plot_wing import plot_wing_3d
from analysis.design_assessment import evaluate_design


def main():
    """
    Run the AeroDesignX aircraft analysis.
    """

    # --------------------------------------------------
    # Airfoil generation
    # --------------------------------------------------

    airfoil = NACA4Airfoil(AIRFOIL)

    upper_surface, lower_surface = airfoil.generate_coordinates()

    plot_airfoil(
        upper_surface,
        lower_surface,
    )

    # --------------------------------------------------
    # Wing generation
    # --------------------------------------------------

    wing = Wing(
        span=WING_SPAN,
        root_chord=ROOT_CHORD,
        tip_chord=TIP_CHORD,
        airfoil=AIRFOIL,
        sweep=SWEEP,
        dihedral=DIHEDRAL,
    )

    wing.display_info()

    plot_wing_3d(
        wing,
        show_full_wing=True,
    )

    # --------------------------------------------------
    # Basic aircraft properties
    # --------------------------------------------------

    weight = MASS * GRAVITY
    wing_area = wing.area
    aspect_ratio = wing.aspect_ratio()
    mean_aerodynamic_chord = wing.mean_aerodynamic_chord()

    # --------------------------------------------------
    # Lift calculations
    # --------------------------------------------------

    lift_required = required_lift(
        mass=MASS,
        gravity=GRAVITY,
    )

    required_cl_value = required_cl(
        mass=MASS,
        gravity=GRAVITY,
        air_density=AIR_DENSITY,
        velocity=CRUISE_SPEED,
        wing_area=wing_area,
    )

    # --------------------------------------------------
    # Drag calculations
    # --------------------------------------------------

    induced_cd = induced_drag_coefficient(
        cl=required_cl_value,
        aspect_ratio=aspect_ratio,
    )

    total_cd = total_drag_coefficient(
        cl=required_cl_value,
        aspect_ratio=aspect_ratio,
    )

    drag = drag_force(
        air_density=AIR_DENSITY,
        velocity=CRUISE_SPEED,
        wing_area=wing_area,
        cd=total_cd,
    )

    lift_drag_ratio = lift_to_drag_ratio(
        lift=lift_required,
        drag=drag,
    )

    # --------------------------------------------------
    # Performance calculations
    # --------------------------------------------------

    wing_loading_value = wing_loading(
        weight=weight,
        wing_area=wing_area,
    )

    stall_speed_value = stall_speed(
        weight=weight,
        air_density=AIR_DENSITY,
        wing_area=wing_area,
        cl_max=CL_MAX,
    )

    stall_margin = stall_speed_margin(
        cruise_speed=CRUISE_SPEED,
        stall_speed_value=stall_speed_value,
    )

    reynolds_value = reynolds_number(
        rho=AIR_DENSITY,
        velocity=CRUISE_SPEED,
        chord=mean_aerodynamic_chord,
    )

    endurance_hours = estimate_endurance(
    battery_capacity_wh=BATTERY_CAPACITY_WH,
    average_power_w=AVERAGE_POWER_W,
    usable_fraction=BATTERY_USABLE_FRACTION,
    )

    range_km = estimate_range(
    cruise_speed=CRUISE_SPEED,
    endurance_hours=endurance_hours,
    )

    # --------------------------------------------------
    # Stall-margin assessment
    # --------------------------------------------------

    if stall_margin < 1.3:
        print("\nWARNING: Cruise speed is too close to stall speed.")
    elif stall_margin < 1.5:
        print("\nCAUTION: Cruise stall margin is limited.")
    else:
        print("\nCruise speed has an acceptable stall margin.")

    # --------------------------------------------------
    # Performance report
    # --------------------------------------------------


    print_performance_report(
        aircraft_name=AIRCRAFT_NAME,
        mass=MASS,
        weight=weight,
        cruise_speed=CRUISE_SPEED,
        wing=wing,
        reynolds_number=reynolds_value,
        required_cl=required_cl_value,
        induced_cd=induced_cd,
        total_cd=total_cd,
        drag_force=drag,
        lift_to_drag=lift_drag_ratio,
        wing_loading=wing_loading_value,
        stall_speed=stall_speed_value,
        stall_margin=stall_margin,
        battery_capacity_wh=BATTERY_CAPACITY_WH,
        average_power_w=AVERAGE_POWER_W,
        endurance_hours=endurance_hours,
        range_km=range_km,
    )

    evaluate_design(
    required_cl=required_cl_value,
    lift_to_drag=lift_drag_ratio,
    stall_margin=stall_margin,
    wing_loading=wing_loading_value,
    )

    # --------------------------------------------------
    # Performance plots
    # --------------------------------------------------

    plot_drag_polar(
        aspect_ratio=aspect_ratio,
        operating_cl=required_cl_value,
    )

    plot_lift_curve(
        operating_cl=required_cl_value,
        cl_max=CL_MAX,
    )

    plot_performance_curves(
        mass=MASS,
        gravity=GRAVITY,
        air_density=AIR_DENSITY,
        wing_area=wing_area,
        aspect_ratio=aspect_ratio,
        cruise_speed=CRUISE_SPEED,
    )


if __name__ == "__main__":
    main()

