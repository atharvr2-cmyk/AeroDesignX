"""
Aircraft Concept Comparison Plots

Creates visual comparisons of the generated and
ranked aircraft concepts.
"""

import matplotlib.pyplot as plt


def plot_metric(
    ranked_results,
    metric_key,
    title,
    ylabel
):
    """
    Plot one performance metric for all aircraft concepts.
    """

    names = [
        result["name"]
        for result in ranked_results
    ]

    values = [
        result[metric_key]
        for result in ranked_results
    ]

    plt.figure(figsize=(10, 6))

    plt.bar(names, values)

    plt.title(title)
    plt.xlabel("Aircraft Concept")
    plt.ylabel(ylabel)

    plt.xticks(rotation=20)
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.show()


def plot_concept_comparison(ranked_results):
    """
    Display several aircraft concept comparison plots.
    """

    plot_metric(
        ranked_results=ranked_results,
        metric_key="score",
        title="Aircraft Concept Design Scores",
        ylabel="Score"
    )

    plot_metric(
        ranked_results=ranked_results,
        metric_key="lift_to_drag",
        title="Aircraft Concept Lift-to-Drag Ratios",
        ylabel="Lift-to-Drag Ratio"
    )

    plot_metric(
        ranked_results=ranked_results,
        metric_key="stall_speed",
        title="Aircraft Concept Stall Speeds",
        ylabel="Stall Speed (m/s)"
    )

    plot_metric(
        ranked_results=ranked_results,
        metric_key="drag",
        title="Aircraft Concept Cruise Drag",
        ylabel="Drag (N)"
    )

    plot_metric(
        ranked_results=ranked_results,
        metric_key="wing_loading",
        title="Aircraft Concept Wing Loading",
        ylabel="Wing Loading (N/m²)"
    )