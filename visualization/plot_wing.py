"""
3D Wing Visualization

Provides functions for visualizing generated wing geometry.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_wing_3d(
    wing,
    show_full_wing=True,
    ax=None,
    show=True,
    save_path="docs/images/wing_geometry.png",
):
    """
    Plot the wing as a three-dimensional surface.

    Parameters
    ----------
    wing : Wing
        Wing object containing geometry and airfoil information.

    show_full_wing : bool, optional
        If True, display the complete mirrored wing.
        If False, display only the right half-wing.

    ax : matplotlib.axes.Axes, optional
        Three-dimensional axes on which to draw the wing.
        If no axes are supplied, the function creates a new
        three-dimensional figure and axes.

    show : bool, optional
        If True, display the figure when this function creates it.

    save_path : str or None, optional
        File path used to save the standalone wing image.
        Set to None to disable saving.

    Returns
    -------
    matplotlib.axes.Axes
        The three-dimensional axes containing the wing plot.
    """

    root_section, tip_section = wing.generate_sections()

    root = np.asarray(root_section, dtype=float)
    tip = np.asarray(tip_section, dtype=float)

    if root.ndim != 2 or root.shape[1] != 3:
        raise ValueError(
            "Root section must contain 3D coordinates."
        )

    if tip.ndim != 2 or tip.shape[1] != 3:
        raise ValueError(
            "Tip section must contain 3D coordinates."
        )

    if root.shape != tip.shape:
        raise ValueError(
            "Root and tip sections must contain "
            "the same number of points."
        )

    created_figure = False

    if ax is None:
        figure = plt.figure(figsize=(11, 7))
        ax = figure.add_subplot(111, projection="3d")
        created_figure = True
    elif not hasattr(ax, "get_zlim3d"):
        raise ValueError(
            "The supplied axes must be three-dimensional."
        )

    x_right = np.vstack((root[:, 0], tip[:, 0]))
    y_right = np.vstack((root[:, 1], tip[:, 1]))
    z_right = np.vstack((root[:, 2], tip[:, 2]))

    ax.plot_surface(
        x_right,
        y_right,
        z_right,
        alpha=0.8,
        edgecolor="black",
        linewidth=0.25,
    )

    ax.plot(
        root[:, 0],
        root[:, 1],
        root[:, 2],
        linewidth=1.5,
        label="Root Section",
    )

    ax.plot(
        tip[:, 0],
        tip[:, 1],
        tip[:, 2],
        linewidth=1.5,
        label="Right Tip Section",
    )

    if show_full_wing:
        left_tip = tip.copy()

        left_tip[:, 1] *= -1

        x_left = np.vstack((root[:, 0], left_tip[:, 0]))
        y_left = np.vstack((root[:, 1], left_tip[:, 1]))
        z_left = np.vstack((root[:, 2], left_tip[:, 2]))

        ax.plot_surface(
            x_left,
            y_left,
            z_left,
            alpha=0.8,
            edgecolor="black",
            linewidth=0.25,
        )

        ax.plot(
            left_tip[:, 0],
            left_tip[:, 1],
            left_tip[:, 2],
            linewidth=1.5,
            label="Left Tip Section",
        )

    ax.set_title(
        f"AeroDesignX Wing — NACA {wing.airfoil}",
        pad=20,
    )

    ax.set_xlabel("Chordwise Position, X (m)")
    ax.set_ylabel("Spanwise Position, Y (m)")
    ax.set_zlabel("Vertical Position, Z (m)")

    ax.legend()

    _set_equal_axes(ax)
    ax.view_init(elev=24, azim=-55)

    if created_figure:
        ax.figure.tight_layout()

        if save_path is not None:
            ax.figure.savefig(
                save_path,
                dpi=300,
                bbox_inches="tight",
            )

        if show:
            plt.show()

    return ax


def _set_equal_axes(ax):
    """
    Preserve the wing's coordinate limits while using box dimensions
    proportional to the physical geometry.
    """

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])

    minimum_display_range = 0.08 * max(
        x_range,
        y_range,
    )

    ax.set_box_aspect(
        (
            x_range,
            y_range,
            max(z_range, minimum_display_range),
        )
    )