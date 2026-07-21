"""
Optimization History Visualization

Plots the convergence history of the aircraft design optimizer.
"""

import matplotlib.pyplot as plt


def plot_optimization(
    history,
    ax=None,
    show=True,
):
    """
    Plot optimization score versus iteration.

    Parameters
    ----------
    history : list of dict
        Optimization history. Each dictionary must contain
        ``iteration`` and ``score`` keys.

    ax : matplotlib.axes.Axes, optional
        Axes on which to draw the plot. If no axes are supplied,
        the function creates a new figure and axes.

    show : bool, optional
        If True, display the figure when this function creates it.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the completed optimization plot.
    """

    if not history:
        raise ValueError(
            "Optimization history cannot be empty."
        )

    for point in history:
        if "iteration" not in point or "score" not in point:
            raise ValueError(
                "Each history point must contain "
                "'iteration' and 'score' keys."
            )

    created_figure = False

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))
        created_figure = True

    iterations = [
        point["iteration"]
        for point in history
    ]

    scores = [
        point["score"]
        for point in history
    ]

    ax.plot(
        iterations,
        scores,
        linewidth=2,
        label="Best Score",
    )

    ax.scatter(
        iterations[-1],
        scores[-1],
        s=70,
        zorder=3,
        label="Final Best Design",
    )

    ax.set_xlabel("Iteration")
    ax.set_ylabel("Optimization Score")
    ax.set_title("Hill-Climb Optimization")
    ax.grid(True)
    ax.legend()

    if created_figure:
        ax.figure.tight_layout()

        if show:
            plt.show()

    return ax