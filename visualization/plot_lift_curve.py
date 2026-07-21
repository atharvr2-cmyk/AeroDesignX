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
    ax=None,
    show=True,
):
    """
    Plot lift coefficient versus angle of attack.

    Parameters
    ----------
    operating_cl : float, optional
        Current cruise lift coefficient.

    lift_curve_slope : float, optional
        Lift-curve slope in CL per degree.

    zero_lift_angle : float, optional
        Zero-lift angle of attack in degrees.

    stall_angle : float, optional
        Approximate stall angle in degrees.

    cl_max : float, optional
        Maximum lift coefficient.

    ax : matplotlib.axes.Axes, optional
        Axes on which to draw the plot. If no axes are supplied,
        the function creates a new figure and axes.

    show : bool, optional
        If True, display the figure when this function creates it.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the completed lift-curve plot.
    """

    if lift_curve_slope <= 0:
        raise ValueError(
            "Lift-curve slope must be greater than zero."
        )

    if cl_max <= 0:
        raise ValueError("CL max must be greater than zero.")

    if stall_angle <= zero_lift_angle:
        raise ValueError(
            "Stall angle must be greater than the zero-lift angle."
        )

    created_figure = False

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 6))
        created_figure = True

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

    ax.plot(
        alpha_values,
        cl_values,
        linewidth=2,
        label="Lift Curve",
    )

    ax.axvline(
        stall_angle,
        linestyle="--",
        label="Approximate Stall Angle",
    )

    if operating_cl is not None:
        operating_alpha = (
            operating_cl / lift_curve_slope
            + zero_lift_angle
        )

        ax.scatter(
            operating_alpha,
            operating_cl,
            s=70,
            zorder=3,
            label="Cruise Operating Point",
        )

    ax.set_title("Lift Coefficient vs Angle of Attack")
    ax.set_xlabel("Angle of Attack, α (degrees)")
    ax.set_ylabel("Lift Coefficient, $C_L$")
    ax.grid(True)
    ax.legend()

    if created_figure:
        ax.figure.tight_layout()

        if show:
            plt.show()

    return ax