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
    REQUIRED_ENDURANCE_HOURS,
    PAYLOAD_MASS,
    FUSELAGE_MASS,
    TAIL_MASS,
    PROPULSION_MASS,
    AVIONICS_MASS,
    BATTERY_SPECIFIC_ENERGY_WH_PER_KG,
    PROPULSIVE_EFFICIENCY,
    AVIONICS_POWER_W,
    BATTERY_RESERVE_FRACTION,
)
from geometry.wing import Wing
from visualization.performance_report import print_performance_report
from visualization.plot_airfoil import plot_airfoil
from visualization.plot_drag_polar import plot_drag_polar
from visualization.plot_lift_curve import plot_lift_curve
from visualization.plot_performance import plot_performance_curves
from visualization.plot_wing import plot_wing_3d
from analysis.design_assessment import evaluate_design
from analysis.parameter_sweep import sweep_wing_span
from analysis.design_optimizer import optimize_design
from analysis.mission_sizing import size_aircraft_for_mission
from analysis.design_rationale import explain_design


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
    # Wing-span parameter sweep
    # --------------------------------------------------

    span_values = [
        0.8,
        0.9,
        1.0,
        1.1,
        1.2,
        1.3,
        1.4,
    ]

    sweep_results = sweep_wing_span(
        span_values=span_values,
        root_chord=ROOT_CHORD,
        tip_chord=TIP_CHORD,
        airfoil=AIRFOIL,
        sweep=SWEEP,
        dihedral=DIHEDRAL,
        mass=MASS,
        gravity=GRAVITY,
        air_density=AIR_DENSITY,
        cruise_speed=CRUISE_SPEED,
        cl_max=CL_MAX,
    )

    print("\n" + "=" * 96)
    print("WING-SPAN PARAMETER SWEEP")
    print("=" * 96)

    print(
        f"{'Span':<8}"
        f"{'Area':<10}"
        f"{'AR':<10}"
        f"{'CL Req.':<12}"
        f"{'Drag':<12}"
        f"{'L/D':<10}"
        f"{'Stall V':<12}"
        f"{'W/S':<10}"
        f"{'Score':<8}"
    )

    print("-" * 96)

    for result in sweep_results:
        print(
            f"{result['span']:<8.2f}"
            f"{result['wing_area']:<10.3f}"
            f"{result['aspect_ratio']:<10.2f}"
            f"{result['required_cl']:<12.3f}"
            f"{result['drag']:<12.2f}"
            f"{result['lift_to_drag']:<10.2f}"
            f"{result['stall_speed']:<12.2f}"
            f"{result['wing_loading']:<10.2f}"
            f"{result['score']:<8}"
        )
    
    best_result = max(
        sweep_results,
        key=lambda result: result["score"],
    )

    print("-" * 96)
    print("BEST OVERALL WING DESIGN")
    print(f"Wing span:          {best_result['span']:.2f} m")
    print(f"Wing area:          {best_result['wing_area']:.3f} m^2")
    print(f"Aspect ratio:       {best_result['aspect_ratio']:.2f}")
    print(f"Required CL:        {best_result['required_cl']:.3f}")
    print(f"Lift-to-drag ratio: {best_result['lift_to_drag']:.2f}")
    print(f"Stall speed:        {best_result['stall_speed']:.2f} m/s")
    print(f"Wing loading:       {best_result['wing_loading']:.2f} N/m^2")
    print(f"Overall score:      {best_result['score']}/100")


    # --------------------------------------------------
    # Multi-variable design optimization
    # --------------------------------------------------

    optimization_results = optimize_design(
        span_values=[
            0.9,
            1.0,
            1.1,
            1.2,
            1.3,
            1.4,
        ],
        root_chord_values=[
            0.24,
            0.28,
            0.32,
            0.36,
        ],
        tip_chord_values=[
            0.16,
            0.20,
            0.24,
            0.28,
        ],
        cruise_speed_values=[
            12.0,
            14.0,
            16.0,
            18.0,
        ],
        airfoil=AIRFOIL,
        sweep=SWEEP,
        dihedral=DIHEDRAL,
        mass=MASS,
        gravity=GRAVITY,
        air_density=AIR_DENSITY,
        cl_max=CL_MAX,
    )

    best_design = optimization_results[0]

    print("\n" + "=" * 64)
    print("MULTI-VARIABLE DESIGN OPTIMIZATION")
    print("=" * 64)

    print(
        f"Candidate designs evaluated: "
        f"{len(optimization_results)}"
    )

    print("\nBEST CANDIDATE DESIGN")
    print("-" * 64)
    print(f"Wing span:          {best_design['span']:.2f} m")
    print(f"Root chord:         {best_design['root_chord']:.2f} m")
    print(f"Tip chord:          {best_design['tip_chord']:.2f} m")
    print(f"Cruise speed:       {best_design['cruise_speed']:.2f} m/s")
    print(f"Wing area:          {best_design['wing_area']:.3f} m^2")
    print(f"Aspect ratio:       {best_design['aspect_ratio']:.2f}")
    print(f"Required CL:        {best_design['required_cl']:.3f}")
    print(f"Total CD:           {best_design['total_cd']:.4f}")
    print(f"Drag:               {best_design['drag']:.2f} N")
    print(f"Lift-to-drag ratio: {best_design['lift_to_drag']:.2f}")
    print(f"Stall speed:        {best_design['stall_speed']:.2f} m/s")
    print(f"Stall margin:       {best_design['stall_margin']:.2f}")
    print(f"Wing loading:       {best_design['wing_loading']:.2f} N/m^2")
    print(f"Design score:       {best_design['score']:.2f}/100")

    explain_design(best_design)


    # --------------------------------------------------
    # Iterative mission sizing
    # --------------------------------------------------

    mission_sizing = size_aircraft_for_mission(
        wing=wing,
        initial_mass=MASS,
        gravity=GRAVITY,
        air_density=AIR_DENSITY,
        cruise_speed=CRUISE_SPEED,
        cl_max=CL_MAX,
        endurance_hours=REQUIRED_ENDURANCE_HOURS,
        fuselage_mass=FUSELAGE_MASS,
        tail_mass=TAIL_MASS,
        propulsion_mass=PROPULSION_MASS,
        avionics_mass=AVIONICS_MASS,
        payload_mass=PAYLOAD_MASS,
        battery_specific_energy_wh_per_kg=(
            BATTERY_SPECIFIC_ENERGY_WH_PER_KG
        ),
        propulsive_efficiency=PROPULSIVE_EFFICIENCY,
        avionics_power_w=AVIONICS_POWER_W,
        reserve_fraction=BATTERY_RESERVE_FRACTION,
    )

    print("\n" + "=" * 64)
    print("ITERATIVE MISSION SIZING")
    print("=" * 64)

    print(
        f"Required endurance:  "
        f"{REQUIRED_ENDURANCE_HOURS:.2f} hr"
    )

    print(
        f"Converged:           "
        f"{mission_sizing['converged']}"
    )

    print(
        f"Iterations:          "
        f"{mission_sizing['iterations']}"
    )

    print(
        f"Total aircraft mass: "
        f"{mission_sizing['total_mass']:.3f} kg"
    )

    print(
        f"Wing mass:           "
        f"{mission_sizing['wing_mass']:.3f} kg"
    )

    print(
        f"Battery capacity:    "
        f"{mission_sizing['battery_capacity_wh']:.1f} Wh"
    )

    print(
        f"Battery mass:        "
        f"{mission_sizing['battery_mass']:.3f} kg"
    )

    print(
        f"Electrical power:    "
        f"{mission_sizing['electrical_power_w']:.1f} W"
    )

    print(
        f"Required CL:         "
        f"{mission_sizing['required_cl']:.3f}"
    )

    print(
        f"Cruise drag:         "
        f"{mission_sizing['drag']:.2f} N"
    )

    print(
        f"Stall speed:         "
        f"{mission_sizing['stall_speed']:.2f} m/s"
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

