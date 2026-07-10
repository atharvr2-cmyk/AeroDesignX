def calculate_lift(rho, velocity, wing_area, cl):

    return 0.5 * rho * velocity**2 * wing_area * cl


def calculate_drag(rho, velocity, wing_area, cd):

    return 0.5 * rho * velocity**2 * wing_area * cd