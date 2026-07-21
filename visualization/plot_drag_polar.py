"""
Drag Polar Visualization

Plots drag coefficient versus lift coefficient.
"""

import numpy as np
import matplotlib.pyplot as plt

from aerodynamics.drag import total_drag_coefficient


def plot_drag_polar(
    aspect_ratio,
    cd0=0.03,
    oswald_efficiency=0.8,
    operating_cl=None,
    ax=None,
    show=True,
):
    """
    Plot the aircraft drag polar.

    Parameters
    ----------
    aspect_ratio : float
        Wing aspect ratio.

    cd0 : float, optional
        Zero-lift drag coefficient.

    oswald_efficiency : float, optional
        Oswald efficiency factor.

    operating_cl : float, optional
        Current operating lift coefficient.

    ax : matplotlib.axes.Axes, optional
        Axes on which to draw the plot. If no axes are supplied,
        the function creates a new figure and axes.

    show : bool, optional
        If True, display the figure. This is mainly used when the
        function creates its own figure.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the completed drag-polar plot.
    """

    if aspect_ratio <= 0:
        raise ValueError("Aspect ratio must be greater than zero.")

    if cd0 < 0:
        raise ValueError("CD0 cannot be negative.")

    if oswald_efficiency <= 0:
        raise ValueError(
            "Oswald efficiency must be greater than zero."
        )

    created_figure = False

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 6))
        created_figure = True

    cl_values = np.linspace(-0.5, 1.5, 200)

    cd_values = [
        total_drag_coefficient(
            cl=cl,
            aspect_ratio=aspect_ratio,
            cd0=cd0,
            oswald_efficiency=oswald_efficiency,
        )
        for cl in cl_values
    ]

    ax.plot(
        cd_values,
        cl_values,
        linewidth=2,
        label="Drag Polar",
    )

    if operating_cl is not None:
        operating_cd = total_drag_coefficient(
            cl=operating_cl,
            aspect_ratio=aspect_ratio,
            cd0=cd0,
            oswald_efficiency=oswald_efficiency,
        )

        ax.scatter(
            operating_cd,
            operating_cl,
            s=70,
            zorder=3,
            label="Cruise Operating Point",
        )

    ax.set_title("Aircraft Drag Polar")
    ax.set_xlabel("Drag Coefficient, $C_D$")
    ax.set_ylabel("Lift Coefficient, $C_L$")
    ax.grid(True)
    ax.legend()

    if created_figure:
        ax.figure.tight_layout()

        if show:
            plt.show()

    return ax