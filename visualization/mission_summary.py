"""
Mission Summary Panel

Displays mission feasibility and key mission metrics.
"""

import matplotlib.pyplot as plt


def plot_mission_summary(
    mission_results,
    ax=None,
):
    """
    Display mission evaluation results.

    Parameters
    ----------
    mission_results : dict
        Dictionary returned by evaluate_mission().

    ax : matplotlib.axes.Axes, optional
        Axes used for the summary.

    Returns
    -------
    matplotlib.axes.Axes
        Axes containing the mission summary.
    """

    required_keys = {
        "mission",
        "score",
        "feasible",
        "failed_constraints",
    }

    missing_keys = required_keys - mission_results.keys()

    if missing_keys:
        raise ValueError(
            "Mission results are missing required keys: "
            + ", ".join(sorted(missing_keys))
        )

    if ax is None:
        _, ax = plt.subplots(figsize=(6, 5))

    ax.axis("off")

    status = (
        "PASS"
        if mission_results["feasible"]
        else "FAIL"
    )

    failed_constraints = mission_results[
        "failed_constraints"
    ]

    if failed_constraints:
        formatted_constraints = ", ".join(
            constraint.replace("_", " ").title()
            for constraint in failed_constraints
        )
    else:
        formatted_constraints = "None"

    summary = (
        "Mission Evaluation\n"
        "-----------------------------\n\n"
        f"Mission: {mission_results['mission']}\n"
        f"Status: {status}\n"
        f"Mission Score: "
        f"{mission_results['score']:.1f}/100\n\n"
        f"Failed Constraints:\n"
        f"{formatted_constraints}"
    )

    ax.text(
        0.02,
        0.98,
        summary,
        fontsize=11,
        family="monospace",
        va="top",
    )

    return ax