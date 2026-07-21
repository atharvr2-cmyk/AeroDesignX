"""
Design Summary Panel

Displays important aircraft metrics inside
the engineering dashboard.
"""

import matplotlib.pyplot as plt


def plot_design_summary(
    aircraft,
    ax=None,
):
    """
    Display important aircraft metrics.

    Parameters
    ----------
    aircraft : dict
        Dictionary containing aircraft results.

    ax : matplotlib.axes.Axes
        Axes used to display the summary.
    """

    if ax is None:
        _, ax = plt.subplots(figsize=(6, 5))

    ax.axis("off")

    summary = (
        f"Design Score\n"
        f"-------------------------\n\n"
        f"Score: {aircraft['score']:.1f}/100\n"
        f"Aspect Ratio: {aircraft['aspect_ratio']:.2f}\n"
        f"L/D Ratio: {aircraft['lift_to_drag']:.2f}\n"
        f"Stall Speed: {aircraft['stall_speed']:.2f} m/s\n"
        f"Cruise Speed: {aircraft['cruise_speed']:.2f} m/s\n"
        f"Wing Area: {aircraft['wing_area']:.3f} m²\n"
        f"Required CL: {aircraft['required_cl']:.3f}\n"
        f"Drag: {aircraft['drag']:.2f} N"
    )

    ax.text(
        0.02,
        0.98,
        summary,
        fontsize=11,
        va="top",
        family="monospace",
    )

    return ax