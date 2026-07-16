"""
Design Rationale

Explains why the optimizer selected
the best aircraft.
"""


def explain_design(best_design):
    """
    Print a human-readable explanation
    of the optimized aircraft.
    """

    print("\n" + "=" * 60)
    print("DESIGN RATIONALE")
    print("=" * 60)

    print("\nWhy this aircraft was selected:\n")

    if best_design["required_cl"] < 0.7:
        print("✓ Low required lift coefficient")
    elif best_design["required_cl"] < 1.0:
        print("• Acceptable lift coefficient")
    else:
        print("• High lift coefficient")

    if best_design["lift_to_drag"] > 10:
        print("✓ Excellent aerodynamic efficiency")
    elif best_design["lift_to_drag"] > 8:
        print("• Good aerodynamic efficiency")
    else:
        print("• Aerodynamic efficiency could improve")

    if best_design["stall_margin"] > 1.5:
        print("✓ Large stall safety margin")
    else:
        print("• Limited stall margin")

    wing_loading = best_design["wing_loading"]

    if 80 <= wing_loading <= 100:
        print("✓ Wing loading near conceptual target")
    else:
        print("• Wing loading outside preferred range")

    print(
        "\nOverall Recommendation:\n"
        "This design provides the best balance of\n"
        "efficiency, controllability, and mission performance."
    )