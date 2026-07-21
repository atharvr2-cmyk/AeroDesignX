import matplotlib.pyplot as plt


def plot_optimization(history):
    """
    Plot hill-climb convergence.
    """

    iterations = [
        point["iteration"]
        for point in history
    ]

    scores = [
        point["score"]
        for point in history
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        iterations,
        scores,
        linewidth=2,
    )

    plt.grid(True)

    plt.xlabel("Iteration")

    plt.ylabel("Optimization Score")

    plt.title("Hill-Climb Optimization")

    plt.tight_layout()

    plt.show()