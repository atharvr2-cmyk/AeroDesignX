"""
Aircraft Analysis

Provides high-level engineering checks.
"""

from aerodynamics.lift import required_cl


def evaluate_design(aircraft):
    """
    Evaluate whether the aircraft's required CL
    is within a reasonable operating range.
    """

    cl = required_cl(aircraft)

    print("\n========== Design Evaluation ==========")
    print(f"Required CL: {cl:.3f}")

    if cl < 0.8:
        print("Status: Excellent cruise condition.")

    elif cl < 1.5:
        print("Status: Flyable, but operating at a high lift coefficient.")

    else:
        print("Status: Design is NOT currently feasible.")
        print("Reason: Required CL exceeds typical aerodynamic limits.")

    print("=======================================")