"""
Performance Report

Formats and displays the calculated aircraft
geometry, aerodynamic, and performance results.
"""


def print_performance_report(
    aircraft_name,
    mass,
    weight,
    cruise_speed,
    wing,
    reynolds_number,
    required_cl,
    induced_cd,
    total_cd,
    drag_force,
    lift_to_drag,
    wing_loading,
    stall_speed,
    stall_margin,
):
    """
    Print a formatted aircraft performance report.
    """

    print("\n" + "=" * 54)
    print(f"{aircraft_name:^54}")
    print(f"{'Performance Report':^54}")
    print("=" * 54)

    print("\nAIRCRAFT")
    print("-" * 54)
    print(f"{'Mass:':30}{mass:>12.2f} kg")
    print(f"{'Weight:':30}{weight:>12.2f} N")
    print(f"{'Cruise Speed:':30}{cruise_speed:>12.2f} m/s")

    print("\nWING GEOMETRY")
    print("-" * 54)
    print(f"{'Wing Span:':30}{wing.span:>12.2f} m")
    print(f"{'Wing Area:':30}{wing.area:>12.3f} m²")
    print(f"{'Aspect Ratio:':30}{wing.aspect_ratio():>12.3f}")
    print(
        f"{'Mean Aerodynamic Chord:':30}"
        f"{wing.mean_aerodynamic_chord():>12.3f} m"
    )
    print(f"{'Taper Ratio:':30}{wing.taper_ratio:>12.3f}")
    print(f"{'Sweep:':30}{wing.sweep:>12.1f}°")
    print(f"{'Dihedral:':30}{wing.dihedral:>12.1f}°")
    print(f"{'Airfoil:':30}{wing.airfoil:>12}")

    print("\nAERODYNAMICS")
    print("-" * 54)
    print(f"{'Reynolds Number:':30}{reynolds_number:>12,.0f}")
    print(f"{'Required CL:':30}{required_cl:>12.3f}")
    print(f"{'Induced CD:':30}{induced_cd:>12.4f}")
    print(f"{'Total CD:':30}{total_cd:>12.4f}")
    print(f"{'Drag Force:':30}{drag_force:>12.2f} N")
    print(f"{'Lift-to-Drag Ratio:':30}{lift_to_drag:>12.2f}")

    print("\nPERFORMANCE")
    print("-" * 54)
    print(f"{'Wing Loading:':30}{wing_loading:>12.2f} N/m²")
    print(f"{'Stall Speed:':30}{stall_speed:>12.2f} m/s")
    print(f"{'Cruise/Stall Ratio:':30}{stall_margin:>12.2f}")

    print("\nDESIGN STATUS")
    print("-" * 54)

    if required_cl > 1.4:
        print("FAIL: Required cruise CL exceeds assumed CL maximum.")
    elif stall_margin < 1.3:
        print("WARNING: Cruise speed is too close to stall speed.")
    elif stall_margin < 1.5:
        print("CAUTION: Cruise stall margin is limited.")
    else:
        print("PASS: Cruise stall margin is acceptable.")

    if lift_to_drag < 7:
        print("CAUTION: Aerodynamic efficiency is relatively low.")
    else:
        print("PASS: Aerodynamic efficiency is acceptable.")

    print("=" * 54)