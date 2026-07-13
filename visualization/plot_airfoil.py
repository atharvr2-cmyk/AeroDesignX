import matplotlib.pyplot as plt


def plot_airfoil(upper, lower):

    x_upper = [p[0] for p in upper]
    y_upper = [p[1] for p in upper]

    x_lower = [p[0] for p in lower]
    y_lower = [p[1] for p in lower]

    plt.figure(figsize=(10, 3))

    plt.plot(x_upper, y_upper)
    plt.plot(x_lower, y_lower)

    plt.gca().set_aspect("equal")

    plt.grid(True)

    plt.title("Generated NACA Airfoil")

    plt.xlabel("Chord")

    plt.ylabel("Thickness")

    plt.show()