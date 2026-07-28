"""
Configuration-Specific Geometry

Provides baseline wing geometry values for Conventional,
Twin Boom, and Flying Wing aircraft layouts.
"""


def get_configuration_geometry(configuration_name):
    """
    Return baseline wing geometry for the selected aircraft configuration.
    """

    configuration_geometry = {
        "Conventional": {
            "span": 1.20,
            "root_chord": 0.36,
            "tip_chord": 0.20,
            "sweep": 0.0,
            "dihedral": 5.0,
            "airfoil": "4412",
        },

        "Twin Boom": {
            "span": 1.40,
            "root_chord": 0.34,
            "tip_chord": 0.20,
            "sweep": 3.0,
            "dihedral": 3.0,
            "airfoil": "4412",
        },

        "Flying Wing": {
            "span": 1.20,
            "root_chord": 0.48,
            "tip_chord": 0.18,
            "sweep": 25.0,
            "dihedral": 2.0,
            "airfoil": "0012",
        },
    }

    if configuration_name not in configuration_geometry:
        raise ValueError(
            f"Unknown aircraft configuration: {configuration_name}"
        )

    return configuration_geometry[configuration_name]