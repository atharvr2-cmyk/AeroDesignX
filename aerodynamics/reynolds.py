"""
Reynolds Number Calculations
"""

AIR_VISCOSITY = 1.81e-5  # Pa·s


def reynolds_number(rho, velocity, chord, mu=AIR_VISCOSITY):
    """
    Calculate Reynolds number.

    Parameters
    ----------
    rho : float
        Air density (kg/m³)

    velocity : float
        Flight speed (m/s)

    chord : float
        Mean aerodynamic chord (m)

    mu : float
        Dynamic viscosity (Pa·s)

    Returns
    -------
    float
        Reynolds number
    """

    return (rho * velocity * chord) / mu