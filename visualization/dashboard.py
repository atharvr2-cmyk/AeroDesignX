"""
AeroDesignX Engineering Dashboard

Combines aircraft geometry, aerodynamic plots,
optimization history, and key design metrics.
"""

import matplotlib.pyplot as plt

from visualization.design_summary import (
    plot_design_summary,
)
from visualization.plot_drag_polar import (
    plot_drag_polar,
)
from visualization.plot_lift_curve import (
    plot_lift_curve,
)
from visualization.plot_optimization import (
    plot_optimization,
)
from visualization.plot_wing import (
    plot_wing_3d,
)
from visualization.mission_summary import (
    plot_mission_summary,
)

def plot_design_dashboard(
    wing,
    operating_cl,
    optimization_history,
    aircraft_results,
    mission_results,
    cd0=0.03,
    oswald_efficiency=0.8,
    show=True,
    save_path="docs/images/design_dashboard.png",
):
    """
    Create the AeroDesignX engineering dashboard.

    Parameters
    ----------
    wing : Wing
        Wing object used for geometry and aspect ratio.

    operating_cl : float
        Cruise operating lift coefficient.

    optimization_history : list of dict
        Optimization history containing iteration and score values.

    aircraft_results : dict
        Optimized aircraft results displayed in the summary panel.

    cd0 : float, optional
        Zero-lift drag coefficient.

    oswald_efficiency : float, optional
        Oswald efficiency factor.

    show : bool, optional
        If True, display the completed dashboard.

    save_path : str or None, optional
        File path used to save the dashboard.
        Set to None to disable saving.

    Returns
    -------
    matplotlib.figure.Figure
        Completed dashboard figure.
    """

    if wing is None:
        raise ValueError(
            "A wing object must be provided."
        )

    if operating_cl is None:
        raise ValueError(
            "An operating lift coefficient must be provided."
        )

    if not optimization_history:
        raise ValueError(
            "Optimization history cannot be empty."
        )

    if not aircraft_results:
        raise ValueError(
            "Aircraft results cannot be empty."
        )
    
    if not mission_results:
        raise ValueError(
            "Mission results cannot be empty."
        )

    figure = plt.figure(
        figsize=(17, 15),
        constrained_layout=True,
    )

    grid = figure.add_gridspec(
        nrows=3,
        ncols=2,
    )

    wing_ax = figure.add_subplot(
        grid[0, 0],
        projection="3d",
    )

    drag_ax = figure.add_subplot(
        grid[0, 1],
    )

    lift_ax = figure.add_subplot(
        grid[1, 0],
    )

    summary_ax = figure.add_subplot(
        grid[1, 1],
    )

    mission_ax = figure.add_subplot(
        grid[2, 0],
    )

    optimization_ax = figure.add_subplot(
        grid[2, 1],
    )

    plot_wing_3d(
        wing=wing,
        show_full_wing=True,
        ax=wing_ax,
        show=False,
        save_path=None,
    )

    plot_drag_polar(
        aspect_ratio=wing.aspect_ratio(),
        cd0=cd0,
        oswald_efficiency=oswald_efficiency,
        operating_cl=operating_cl,
        ax=drag_ax,
        show=False,
    )

    plot_lift_curve(
        operating_cl=operating_cl,
        ax=lift_ax,
        show=False,
    )

    plot_design_summary(
        aircraft=aircraft_results,
        ax=summary_ax,
    )

    plot_mission_summary(
        mission_results=mission_results,
        ax=mission_ax,
    )

    plot_optimization(
        history=optimization_history,
        ax=optimization_ax,
        show=False,
    )

    figure.suptitle(
        "AeroDesignX — Aircraft Design Dashboard",
        fontsize=18,
        fontweight="bold",
    )

    if save_path is not None:
        figure.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight",
        )

    if show:
        plt.show()

    return figure