"""
Aircraft Performance Visualization

Plots lift and drag force across a range of flight speeds.
"""

import numpy as np
import matplotlib.pyplot as plt

from aerodynamics.lift import required_cl
from aerodynamics.drag import total_drag_coefficient, drag_force


def plot_performance_curves(
    mass,
    gravity,
    air_density,
    wing_area,
    aspect_ratio,
    cruise_speed,
    cd0=0.03,
    oswald_efficiency=0.8,
):
    """
    Plot required lift coefficient and drag force
    across a range of flight speeds.
    """

    speeds = np.linspace(5.0, 30.0, 150)

    cl_values = []
    drag_values = []

    for speed in speeds:
        cl = required_cl(
            mass=mass,
            gravity=gravity,
            air_density=air_density,
            velocity=speed,
            wing_area=wing_area,
        )

        cd = total_drag_coefficient(
            cl=cl,
            aspect_ratio=aspect_ratio,
            cd0=cd0,
            oswald_efficiency=oswald_efficiency,
        )

        drag = drag_force(
            air_density=air_density,
            velocity=speed,
            wing_area=wing_area,
            cd=cd,
        )

        cl_values.append(cl)
        drag_values.append(drag)

    plt.figure(figsize=(8, 6))

    plt.plot(
        speeds,
        drag_values,
        label="Drag Force",
    )

    plt.axvline(
        cruise_speed,
        linestyle="--",
        label="Cruise Speed",
    )

    plt.title("Drag Force vs Flight Speed")
    plt.xlabel("Flight Speed (m/s)")
    plt.ylabel("Drag Force (N)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 6))

    plt.plot(
        speeds,
        cl_values,
        label="Required Lift Coefficient",
    )

    plt.axvline(
        cruise_speed,
        linestyle="--",
        label="Cruise Speed",
    )

    plt.title("Required Lift Coefficient vs Flight Speed")
    plt.xlabel("Flight Speed (m/s)")
    plt.ylabel("Required Lift Coefficient, $C_L$")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()