# import config
from aerodynamics.lift import required_lift
from aerodynamics.performance import dynamic_pressure
from aerodynamics.lift import required_cl
from aerodynamics.analysis import evaluate_design
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from airfoils.naca import NACA4Airfoil
from geometry.wing import Wing
from visualization.plot_wing import plot_wing_3d
from aerodynamics.reynolds import reynolds_number
from config.parameters import (
    AIR_DENSITY,
    CRUISE_SPEED,
    WING_SPAN,
    ROOT_CHORD,
    TIP_CHORD,
    DIHEDRAL,
    SWEEP,
    AIRFOIL,
    MASS,
    GRAVITY,
    CL_MAX,
    AIRCRAFT_NAME
)
from aerodynamics.lift import required_lift, required_cl
from aerodynamics.drag import (
    induced_drag_coefficient,
    total_drag_coefficient,
    drag_force,
)
from aerodynamics.performance import (
    dynamic_pressure,
    wing_loading,
    stall_speed,
    lift_to_drag_ratio,
    stall_speed_margin,
)
from visualization.performance_report import print_performance_report
from visualization.plot_drag_polar import plot_drag_polar
from visualization.plot_lift_curve import plot_lift_curve
from visualization.plot_performance import plot_performance_curves
# from aircraft import Aircraft

# from aerodynamics.aerodynamics import (
#     calculate_lift,
#     calculate_drag
# )

# # ---------------------------------------------

# uav = Aircraft()

# lift = calculate_lift(
#     config.AIR_DENSITY,
#     uav.speed,
#     uav.wing_area,
#     uav.cl
# )

# drag = calculate_drag(
#     config.AIR_DENSITY,
#     uav.speed,
#     uav.wing_area,
#     uav.cd
# )

# # ---------------------------------------------

# print("=" * 45)
# print("           AeroDesignX")
# print("=" * 45)

# print()

# print(f"Mass              : {uav.mass:.2f} kg")
# print(f"Weight            : {uav.weight:.2f} N")

# print(f"Payload           : {uav.payload:.2f} kg")

# print(f"Cruise Speed      : {uav.speed:.2f} m/s")

# print()

# print(f"Wing Area         : {uav.wing_area:.2f} m²")
# print(f"Aspect Ratio      : {uav.aspect_ratio:.2f}")

# print()

# print(f"Lift              : {lift:.2f} N")
# print(f"Drag              : {drag:.2f} N")

# print()

# print("=" * 45)

# from config.parameters import *


# print("Aircraft:", AIRCRAFT_NAME)
# print("Mass:", MASS, "kg")
# print("Wing Span:", WING_SPAN, "m")
# print("Cruise Speed:", CRUISE_SPEED, "m/s")

# from aircraft.assembly import Aircraft


# def main():
#     aircraft = Aircraft()

#     aircraft.display_info()

#     lift = required_lift(aircraft)
#     print(f"\nRequired Lift: {lift:.2f} N") 

#     q = dynamic_pressure(aircraft)
#     print(f"Dynamic Pressure: {q:.2f} Pa")

#     cl = required_cl(aircraft)
#     print(f"Required CL: {cl:.3f}")

#     evaluate_design(aircraft)

# if __name__ == "__main__":
#     main()


# from airfoils.loader import AirfoilLoader

# from airfoils.naca import NACA4Airfoil

# airfoil = NACA4Airfoil("4412")

# airfoil.display_info()

# loader = AirfoilLoader("airfoils/naca4412.dat")

# coordinates = loader.load_coordinates()

# print(f"\nLoaded {len(coordinates)} airfoil coordinates.\n")

# print("First five coordinates:")

# for point in coordinates[:5]:
#     print(point)

from airfoils.naca import NACA4Airfoil
from visualization.plot_airfoil import plot_airfoil

airfoil = NACA4Airfoil("4412")

upper, lower = airfoil.generate_coordinates()

plot_airfoil(upper, lower)

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


mean_chord = (wing.root_chord + wing.tip_chord) / 2

reynolds = reynolds_number(
    rho=AIR_DENSITY,
    velocity=CRUISE_SPEED,
    chord=mean_chord,
)

# print(f"\nMean Chord: {mean_chord:.3f} m")
# print(f"Reynolds Number: {reynolds:,.0f}")


wing_area = wing.area

# print(f"Wing Area: {wing_area:.3f} m²")


lift_required = required_lift(
    mass=MASS,
    gravity=GRAVITY,
)

required_cl_value = required_cl(
    mass=MASS,
    gravity=GRAVITY,
    air_density=AIR_DENSITY,
    velocity=CRUISE_SPEED,
    wing_area=wing.area,
)

# print(f"Required Lift: {lift_required:.2f} N")
# print(f"Required CL: {required_cl_value:.3f}")


aspect_ratio = wing.aspect_ratio()

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
    wing_area=wing.area,
    cd=total_cd,
)

# print(f"Aspect Ratio: {aspect_ratio:.3f}")
# print(f"Induced Drag Coefficient: {induced_cd:.4f}")
# print(f"Total Drag Coefficient: {total_cd:.4f}")
# print(f"Drag Force: {drag:.2f} N")

weight = MASS * GRAVITY

wing_loading_value = wing_loading(
    weight=weight,
    wing_area=wing.area,
)

stall_speed_value = stall_speed(
    weight=weight,
    air_density=AIR_DENSITY,
    wing_area=wing.area,
    cl_max=CL_MAX,
)

# print(f"Wing Loading: {wing_loading_value:.2f} N/m²")
# print(f"Stall Speed: {stall_speed_value:.2f} m/s")

lift_drag_ratio = lift_to_drag_ratio(
    lift=lift_required,
    drag=drag,
)

# print(f"Lift-to-Drag Ratio: {lift_drag_ratio:.2f}")

stall_margin = stall_speed_margin(
    cruise_speed=CRUISE_SPEED,
    stall_speed_value=stall_speed_value,
)

# print(f"Cruise/Stall Speed Ratio: {stall_margin:.2f}")

if stall_margin < 1.3:
    print("WARNING: Cruise speed is too close to stall speed.")
elif stall_margin < 1.5:
    print("CAUTION: Cruise stall margin is limited.")
else:
    print("Cruise speed has an acceptable stall margin.")


mean_aerodynamic_chord = wing.mean_aerodynamic_chord()

reynolds = reynolds_number(
    rho=AIR_DENSITY,
    velocity=CRUISE_SPEED,
    chord=mean_aerodynamic_chord,
)

print_performance_report(
    aircraft_name=AIRCRAFT_NAME,
    mass=MASS,
    weight=weight,
    cruise_speed=CRUISE_SPEED,
    wing=wing,
    reynolds_number=reynolds,
    required_cl=required_cl_value,
    induced_cd=induced_cd,
    total_cd=total_cd,
    drag_force=drag,
    lift_to_drag=lift_drag_ratio,
    wing_loading=wing_loading_value,
    stall_speed=stall_speed_value,
    stall_margin=stall_margin,
)

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
    wing_area=wing.area,
    aspect_ratio=aspect_ratio,
    cruise_speed=CRUISE_SPEED,
)