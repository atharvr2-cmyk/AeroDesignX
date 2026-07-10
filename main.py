# import config
from aerodynamics.lift import required_lift
from aerodynamics.performance import dynamic_pressure
from aerodynamics.lift import required_cl
from aerodynamics.analysis import evaluate_design
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

from aircraft.assembly import Aircraft


def main():
    aircraft = Aircraft()

    aircraft.display_info()

    lift = required_lift(aircraft)
    print(f"\nRequired Lift: {lift:.2f} N") 

    q = dynamic_pressure(aircraft)
    print(f"Dynamic Pressure: {q:.2f} Pa")

    cl = required_cl(aircraft)
    print(f"Required CL: {cl:.3f}")

    evaluate_design(aircraft)

if __name__ == "__main__":
    main()