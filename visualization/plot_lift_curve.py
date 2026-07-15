"""
Lift Curve Visualization

Plots lift coefficient versus angle of attack.
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_lift_curve(
    operating_cl=None,
    lift_curve_slope=0.1,
    zero_lift_angle=-3.0,
    stall_angle=14.0,
    cl_max=1.4,
):
    """
    Plot lift coefficient versus angle of attack.

    Parameters
    ----------
    operating_cl : float, optional
        Current cruise lift coefficient.

    lift_curve_slope : float
        Lift curve slope in CL per degree.

    zero_lift_angle : float
        Zero-lift angle of attack in degrees.

    stall_angle : float
        Approximate stall angle in degrees.

    cl_max : float
        Maximum lift coefficient.
    """

    alpha_values = np.linspace(-8, 20, 200)

    cl_values = []

    for alpha in alpha_values:
        linear_cl = lift_curve_slope * (
            alpha - zero_lift_angle
        )

        if alpha <= stall_angle:
            cl = min(linear_cl, cl_max)
        else:
            cl = cl_max - 0.08 * (
                alpha - stall_angle
            )

        cl_values.append(cl)

    plt.figure(figsize=(8, 6))

    plt.plot(
        alpha_values,
        cl_values,
        label="Lift Curve",
    )

    plt.axvline(
        stall_angle,
        linestyle="--",
        label="Approximate Stall Angle",
    )

    if operating_cl is not None:
        operating_alpha = (
            operating_cl / lift_curve_slope
            + zero_lift_angle
        )

        plt.scatter(
            operating_alpha,
            operating_cl,
            s=70,
            label="Cruise Operating Point",
        )

    plt.title("Lift Coefficient vs Angle of Attack")
    plt.xlabel("Angle of Attack, α (degrees)")
    plt.ylabel("Lift Coefficient, $C_L$")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()