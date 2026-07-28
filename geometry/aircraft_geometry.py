"""Generate coordinate-based aircraft geometry for visualization and CAD export."""

from math import radians, tan


def generate_wing_coordinates(
    span: float,
    root_chord: float,
    tip_chord: float,
    sweep_deg: float = 0.0,
    dihedral_deg: float = 0.0,
) -> dict:
    """
    Generate the main corner coordinates of a symmetric tapered wing.

    Coordinate system:
        x = aircraft longitudinal direction
        y = left/right spanwise direction
        z = vertical direction

    Args:
        span: Total wingspan in meters.
        root_chord: Wing chord at the aircraft centerline in meters.
        tip_chord: Wing chord at each wingtip in meters.
        sweep_deg: Leading-edge sweep angle in degrees.
        dihedral_deg: Wing dihedral angle in degrees.

    Returns:
        Dictionary containing the wing's main coordinates.
    """

    if span <= 0:
        raise ValueError("Wing span must be greater than zero.")

    if root_chord <= 0 or tip_chord <= 0:
        raise ValueError("Wing chords must be greater than zero.")

    semi_span = span / 2.0

    sweep_offset = semi_span * tan(radians(sweep_deg))
    tip_height = semi_span * tan(radians(dihedral_deg))

    center_le = (0.0, 0.0, 0.0)
    center_te = (root_chord, 0.0, 0.0)

    right_tip_le = (
        sweep_offset,
        semi_span,
        tip_height,
    )

    right_tip_te = (
        sweep_offset + tip_chord,
        semi_span,
        tip_height,
    )

    left_tip_le = (
        sweep_offset,
        -semi_span,
        tip_height,
    )

    left_tip_te = (
        sweep_offset + tip_chord,
        -semi_span,
        tip_height,
    )

    return {
        "span": span,
        "semi_span": semi_span,
        "root_chord": root_chord,
        "tip_chord": tip_chord,
        "sweep_deg": sweep_deg,
        "dihedral_deg": dihedral_deg,
        "center_le": center_le,
        "center_te": center_te,
        "right_tip_le": right_tip_le,
        "right_tip_te": right_tip_te,
        "left_tip_le": left_tip_le,
        "left_tip_te": left_tip_te,
    }


def print_wing_coordinates(wing_geometry: dict) -> None:
    """Print wing coordinates in an organized format."""

    print("\n" + "=" * 72)
    print("WING GEOMETRY COORDINATES")
    print("=" * 72)

    print(f"Total Span:        {wing_geometry['span']:.3f} m")
    print(f"Semi-Span:         {wing_geometry['semi_span']:.3f} m")
    print(f"Root Chord:        {wing_geometry['root_chord']:.3f} m")
    print(f"Tip Chord:         {wing_geometry['tip_chord']:.3f} m")
    print(f"Leading-Edge Sweep:{wing_geometry['sweep_deg']:.2f} deg")
    print(f"Dihedral:          {wing_geometry['dihedral_deg']:.2f} deg")

    print("\nCOORDINATES")
    print("-" * 72)

    coordinate_names = [
        ("Center Leading Edge", "center_le"),
        ("Center Trailing Edge", "center_te"),
        ("Right Tip Leading Edge", "right_tip_le"),
        ("Right Tip Trailing Edge", "right_tip_te"),
        ("Left Tip Leading Edge", "left_tip_le"),
        ("Left Tip Trailing Edge", "left_tip_te"),
    ]

    for display_name, key in coordinate_names:
        x, y, z = wing_geometry[key]

        print(
            f"{display_name:<28}"
            f"x = {x:>7.3f} m, "
            f"y = {y:>7.3f} m, "
            f"z = {z:>7.3f} m"
        )

    print("=" * 72)


def plot_wing_planform(wing_geometry: dict) -> None:
    """Plot the wing planform from above using Matplotlib."""

    import matplotlib.pyplot as plt

    center_le = wing_geometry["center_le"]
    center_te = wing_geometry["center_te"]

    right_tip_le = wing_geometry["right_tip_le"]
    right_tip_te = wing_geometry["right_tip_te"]

    left_tip_le = wing_geometry["left_tip_le"]
    left_tip_te = wing_geometry["left_tip_te"]

    x_coordinates = [
        left_tip_le[0],
        center_le[0],
        right_tip_le[0],
        right_tip_te[0],
        center_te[0],
        left_tip_te[0],
        left_tip_le[0],
    ]

    y_coordinates = [
        left_tip_le[1],
        center_le[1],
        right_tip_le[1],
        right_tip_te[1],
        center_te[1],
        left_tip_te[1],
        left_tip_le[1],
    ]

    plt.figure(figsize=(10, 5))

    plt.plot(
        x_coordinates,
        y_coordinates,
        marker="o",
        linewidth=2,
    )

    plt.fill(
        x_coordinates,
        y_coordinates,
        alpha=0.25,
    )

    plt.axhline(
        y=0.0,
        linestyle="--",
        linewidth=1,
    )

    plt.xlabel("Longitudinal Position, x (m)")
    plt.ylabel("Spanwise Position, y (m)")
    plt.title("Generated Wing Planform")

    plt.axis("equal")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def size_aircraft_components(
    wing_geometry: dict,
    payload_mass: float = 0.0,
    mission_name: str = "General",
) -> dict:
    """
    Estimate fuselage and tail dimensions from the optimized wing.

    These are conceptual-design sizing relationships. They provide
    reasonable starting geometry for visualization and later CAD generation.

    Args:
        wing_geometry:
            Wing coordinate dictionary returned by
            generate_wing_coordinates().

        payload_mass:
            User-requested payload mass in kilograms.

        mission_name:
            Selected mission name, such as Cargo, Survey, Trainer, or Racing.

    Returns:
        Dictionary containing estimated aircraft component dimensions.
    """

    if payload_mass < 0:
        raise ValueError("Payload mass cannot be negative.")

    span = wing_geometry["span"]
    root_chord = wing_geometry["root_chord"]
    tip_chord = wing_geometry["tip_chord"]

    mean_chord = (root_chord + tip_chord) / 2.0

    mission = mission_name.strip().lower()

    # Base fuselage sizing
    fuselage_length = max(
        0.72 * span,
        4.0 * mean_chord,
    )

    fuselage_width = max(
        0.42 * root_chord,
        0.08 * fuselage_length,
    )

    # Mission-based adjustments
    if "cargo" in mission:
        fuselage_length *= 1.10
        fuselage_width *= 1.20

    elif "survey" in mission:
        fuselage_length *= 1.05

    elif "trainer" in mission:
        fuselage_length *= 1.08
        fuselage_width *= 1.05

    elif "racing" in mission:
        fuselage_length *= 0.90
        fuselage_width *= 0.85

    elif "vtol" in mission:
        fuselage_length *= 1.05
        fuselage_width *= 1.15

    # Increase fuselage size for payload volume.
    payload_scale = 1.0 + min(payload_mass, 20.0) * 0.015

    fuselage_length *= payload_scale
    fuselage_width *= payload_scale

    # Horizontal tail sizing
    horizontal_tail_span = 0.34 * span
    horizontal_tail_root_chord = 0.58 * root_chord
    horizontal_tail_tip_chord = 0.60 * horizontal_tail_root_chord

    # Vertical tail sizing for later 3D generation
    vertical_tail_height = 0.12 * span
    vertical_tail_root_chord = 0.75 * horizontal_tail_root_chord
    vertical_tail_tip_chord = 0.40 * vertical_tail_root_chord

    return {
        "fuselage_length": fuselage_length,
        "fuselage_width": fuselage_width,
        "horizontal_tail_span": horizontal_tail_span,
        "horizontal_tail_root_chord": horizontal_tail_root_chord,
        "horizontal_tail_tip_chord": horizontal_tail_tip_chord,
        "vertical_tail_height": vertical_tail_height,
        "vertical_tail_root_chord": vertical_tail_root_chord,
        "vertical_tail_tip_chord": vertical_tail_tip_chord,
    }


def generate_aircraft_layout(
    wing_geometry: dict,
    fuselage_length: float,
    fuselage_width: float,
    horizontal_tail_span: float,
    horizontal_tail_root_chord: float,
    horizontal_tail_tip_chord: float,
    vertical_tail_height: float,
    vertical_tail_root_chord: float,
    vertical_tail_tip_chord: float,
    tail_position: float | None = None,
) -> dict:
    """
    Generate a simplified top-view aircraft layout.

    Args:
        wing_geometry:
            Wing coordinate dictionary returned by
            generate_wing_coordinates().

        fuselage_length:
            Total fuselage length in meters.

        fuselage_width:
            Maximum fuselage width in meters.

        horizontal_tail_span:
            Total horizontal-tail span in meters.

        horizontal_tail_root_chord:
            Horizontal-tail root chord in meters.

        horizontal_tail_tip_chord:
            Horizontal-tail tip chord in meters.

        tail_position:
            Longitudinal position of the horizontal-tail leading edge.
            If omitted, the tail is placed automatically near the rear
            of the fuselage.

    Returns:
        Dictionary containing wing, fuselage, and tail geometry.
    """

    if fuselage_length <= 0:
        raise ValueError("Fuselage length must be greater than zero.")

    if fuselage_width <= 0:
        raise ValueError("Fuselage width must be greater than zero.")

    if horizontal_tail_span <= 0:
        raise ValueError("Horizontal-tail span must be greater than zero.")

    if horizontal_tail_root_chord <= 0:
        raise ValueError(
            "Horizontal-tail root chord must be greater than zero."
        )

    if horizontal_tail_tip_chord <= 0:
        raise ValueError(
            "Horizontal-tail tip chord must be greater than zero."
        )

    wing_root_chord = wing_geometry["root_chord"]

    # Place the wing slightly behind the nose.
    wing_leading_edge_x = 0.30 * fuselage_length

    # Automatically place the tail close to the rear of the fuselage.
    if tail_position is None:
        tail_position = (
            fuselage_length
            - horizontal_tail_root_chord
            - 0.08 * fuselage_length
        )

    tail_semi_span = horizontal_tail_span / 2.0

    # Simplified fuselage outline for top-view plotting.
    fuselage_points = [
        (0.0, 0.0),
        (0.08 * fuselage_length, fuselage_width / 2.0),
        (0.75 * fuselage_length, fuselage_width / 2.0),
        (fuselage_length, 0.0),
        (0.75 * fuselage_length, -fuselage_width / 2.0),
        (0.08 * fuselage_length, -fuselage_width / 2.0),
        (0.0, 0.0),
    ]

    horizontal_tail_points = [
        (
            tail_position,
            -tail_semi_span,
        ),
        (
            tail_position,
            tail_semi_span,
        ),
        (
            tail_position + horizontal_tail_tip_chord,
            tail_semi_span,
        ),
        (
            tail_position + horizontal_tail_root_chord,
            0.0,
        ),
        (
            tail_position + horizontal_tail_tip_chord,
            -tail_semi_span,
        ),
        (
            tail_position,
            -tail_semi_span,
        ),
    ]

    vertical_tail_points = [
        (
            tail_position,
            0.0,
        ),
        (
            tail_position + vertical_tail_root_chord,
            0.0,
        ),
        (
            tail_position + vertical_tail_tip_chord,
            vertical_tail_height,
        ),
        (
            tail_position,
            vertical_tail_height,
        ),
        (
            tail_position,
            0.0,
        ),
    ]

    return {
        "wing_geometry": wing_geometry,
        "fuselage_length": fuselage_length,
        "configuration": "Conventional",
        "fuselage_width": fuselage_width,
        "wing_leading_edge_x": wing_leading_edge_x,
        "wing_root_chord": wing_root_chord,
        "horizontal_tail_span": horizontal_tail_span,
        "horizontal_tail_root_chord": horizontal_tail_root_chord,
        "horizontal_tail_tip_chord": horizontal_tail_tip_chord,
        "tail_position": tail_position,
        "fuselage_points": fuselage_points,
        "horizontal_tail_points": horizontal_tail_points,
        "vertical_tail_height": vertical_tail_height,
        "vertical_tail_root_chord": vertical_tail_root_chord,
        "vertical_tail_tip_chord": vertical_tail_tip_chord,
        "vertical_tail_points": vertical_tail_points,
    }

def generate_flying_wing_layout(
    wing_geometry: dict,
) -> dict:
    """
    Generate a simplified flying-wing aircraft layout.

    A flying wing has no separate fuselage or horizontal tail.
    The swept main wing forms the complete aircraft planform.
    """

    root_chord = wing_geometry["root_chord"]

    return {
        "configuration": "Flying Wing",
        "wing_geometry": wing_geometry,

        # Place the wing nose at x = 0.
        "wing_leading_edge_x": 0.0,
        "wing_root_chord": root_chord,

        # Flying wings do not use a conventional fuselage.
        "fuselage_length": root_chord,
        "fuselage_width": 0.0,
        "fuselage_points": [],

        # No separate horizontal tail.
        "horizontal_tail_span": 0.0,
        "horizontal_tail_root_chord": 0.0,
        "horizontal_tail_tip_chord": 0.0,
        "horizontal_tail_points": [],

        # No conventional vertical tail.
        "vertical_tail_height": 0.0,
        "vertical_tail_root_chord": 0.0,
        "vertical_tail_tip_chord": 0.0,
        "vertical_tail_points": [],
    }

def generate_twin_boom_layout(
    wing_geometry: dict,
    component_sizes: dict,
) -> dict:
    """
    Generate a simplified twin-boom aircraft layout.

    The layout contains a central payload pod, two rear booms,
    and a horizontal tail connecting the booms.
    """

    span = wing_geometry["span"]
    root_chord = wing_geometry["root_chord"]

    fuselage_length = component_sizes["fuselage_length"] * 0.70
    fuselage_width = component_sizes["fuselage_width"]

    horizontal_tail_span = span * 0.50
    horizontal_tail_root_chord = component_sizes[
        "horizontal_tail_root_chord"
    ]
    horizontal_tail_tip_chord = component_sizes[
        "horizontal_tail_tip_chord"
    ]

    wing_leading_edge_x = fuselage_length * 0.25
    wing_trailing_edge_x = wing_leading_edge_x + root_chord

    boom_start_x = wing_trailing_edge_x * 0.85
    boom_end_x = fuselage_length * 1.35
    boom_offset_y = span * 0.22
    boom_width = max(fuselage_width * 0.18, 0.02)

    fuselage_points = [
        (0.0, 0.0),
        (fuselage_length * 0.12, fuselage_width / 2),
        (fuselage_length, fuselage_width / 2),
        (fuselage_length, -fuselage_width / 2),
        (fuselage_length * 0.12, -fuselage_width / 2),
        (0.0, 0.0),
    ]

    left_boom_points = [
        (boom_start_x, -boom_offset_y - boom_width / 2),
        (boom_end_x, -boom_offset_y - boom_width / 2),
        (boom_end_x, -boom_offset_y + boom_width / 2),
        (boom_start_x, -boom_offset_y + boom_width / 2),
        (boom_start_x, -boom_offset_y - boom_width / 2),
    ]

    right_boom_points = [
        (boom_start_x, boom_offset_y - boom_width / 2),
        (boom_end_x, boom_offset_y - boom_width / 2),
        (boom_end_x, boom_offset_y + boom_width / 2),
        (boom_start_x, boom_offset_y + boom_width / 2),
        (boom_start_x, boom_offset_y - boom_width / 2),
    ]

    tail_leading_edge_x = boom_end_x - horizontal_tail_root_chord

    horizontal_tail_points = [
        (
            tail_leading_edge_x,
            -horizontal_tail_span / 2,
        ),
        (
            tail_leading_edge_x,
            horizontal_tail_span / 2,
        ),
        (
            tail_leading_edge_x + horizontal_tail_tip_chord,
            horizontal_tail_span / 2,
        ),
        (
            tail_leading_edge_x + horizontal_tail_root_chord,
            0.0,
        ),
        (
            tail_leading_edge_x + horizontal_tail_tip_chord,
            -horizontal_tail_span / 2,
        ),
        (
            tail_leading_edge_x,
            -horizontal_tail_span / 2,
        ),
    ]

    return {
        "configuration": "Twin Boom",
        "wing_geometry": wing_geometry,
        "wing_leading_edge_x": wing_leading_edge_x,
        "wing_root_chord": root_chord,

        "fuselage_length": fuselage_length,
        "fuselage_width": fuselage_width,
        "fuselage_points": fuselage_points,

        "horizontal_tail_span": horizontal_tail_span,
        "horizontal_tail_root_chord": (
            horizontal_tail_root_chord
        ),
        "horizontal_tail_tip_chord": (
            horizontal_tail_tip_chord
        ),
        "horizontal_tail_points": horizontal_tail_points,

        "vertical_tail_height": component_sizes[
            "vertical_tail_height"
        ],
        "vertical_tail_root_chord": component_sizes[
            "vertical_tail_root_chord"
        ],
        "vertical_tail_tip_chord": component_sizes[
            "vertical_tail_tip_chord"
        ],
        "vertical_tail_points": [],

        "left_boom_points": left_boom_points,
        "right_boom_points": right_boom_points,
    }

def generate_configuration_layout(
    configuration_name: str,
    wing_geometry: dict,
    component_sizes: dict,
) -> dict:
    """
    Route the selected aircraft configuration to the correct
    geometry-generation function.
    """

    if configuration_name == "Conventional":
        return generate_aircraft_layout(
            wing_geometry=wing_geometry,
            **component_sizes,
        )

    if configuration_name == "Flying Wing":
        return generate_flying_wing_layout(
            wing_geometry=wing_geometry,
        )

    if configuration_name == "Twin Boom":
        return generate_twin_boom_layout(
            wing_geometry=wing_geometry,
            component_sizes=component_sizes,
        )

    raise ValueError(
        f"Unknown aircraft configuration: {configuration_name}"
    )

def generate_conventional_side_view(
    aircraft_layout: dict,
) -> dict:
    """
    Generate side-view coordinates for a conventional aircraft.

    The side view contains:
        - Fuselage profile
        - Main-wing profile
        - Horizontal-tail profile
        - Vertical-tail profile
    """

    fuselage_length = aircraft_layout["fuselage_length"]
    fuselage_width = aircraft_layout["fuselage_width"]

    wing_leading_edge_x = aircraft_layout[
        "wing_leading_edge_x"
    ]
    wing_root_chord = aircraft_layout["wing_root_chord"]

    tail_position = aircraft_layout["tail_position"]
    horizontal_tail_chord = aircraft_layout[
        "horizontal_tail_root_chord"
    ]

    vertical_tail_height = aircraft_layout[
        "vertical_tail_height"
    ]
    vertical_tail_root_chord = aircraft_layout[
        "vertical_tail_root_chord"
    ]
    vertical_tail_tip_chord = aircraft_layout[
        "vertical_tail_tip_chord"
    ]

    fuselage_height = 0.65 * fuselage_width
    wing_thickness = 0.12 * wing_root_chord
    tail_thickness = 0.10 * horizontal_tail_chord

    # Side outline of the fuselage.
    fuselage_side_points = [
        (0.0, 0.0),
        (
            0.08 * fuselage_length,
            fuselage_height / 2.0,
        ),
        (
            0.72 * fuselage_length,
            fuselage_height / 2.0,
        ),
        (
            fuselage_length,
            0.0,
        ),
        (
            0.72 * fuselage_length,
            -fuselage_height / 2.0,
        ),
        (
            0.08 * fuselage_length,
            -fuselage_height / 2.0,
        ),
        (0.0, 0.0),
    ]

    # Main wing represented by its root airfoil thickness.
    wing_center_z = 0.0

    # Smooth NACA-style main-wing root profile.
    import numpy as np

    number_of_points = 60
    theta = np.linspace(0.0, np.pi, number_of_points)
    normalized_x = 0.5 * (1.0 - np.cos(theta))

    wing_thickness_ratio = 0.12

    normalized_wing_thickness = (
        5.0
        * wing_thickness_ratio
        * (
            0.2969 * np.sqrt(normalized_x)
            - 0.1260 * normalized_x
            - 0.3516 * normalized_x**2
            + 0.2843 * normalized_x**3
            - 0.1036 * normalized_x**4
        )
    )

    wing_upper_surface = [
        (
            wing_leading_edge_x + x_value * wing_root_chord,
            thickness_value * wing_root_chord,
        )
        for x_value, thickness_value in zip(
            normalized_x,
            normalized_wing_thickness,
        )
    ]

    wing_lower_surface = [
        (
            wing_leading_edge_x + x_value * wing_root_chord,
            -thickness_value * wing_root_chord,
        )
        for x_value, thickness_value in zip(
            reversed(normalized_x),
            reversed(normalized_wing_thickness),
        )
    ]

    wing_side_points = (
        wing_upper_surface
        + wing_lower_surface
        + [wing_upper_surface[0]]
    )

    # Smooth horizontal-tail root profile.
    horizontal_tail_center_z = 0.08 * fuselage_height
    tail_thickness_ratio = 0.10

    normalized_tail_thickness = (
        5.0
        * tail_thickness_ratio
        * (
            0.2969 * np.sqrt(normalized_x)
            - 0.1260 * normalized_x
            - 0.3516 * normalized_x**2
            + 0.2843 * normalized_x**3
            - 0.1036 * normalized_x**4
        )
    )

    tail_upper_surface = [
        (
            tail_position + x_value * horizontal_tail_chord,
            horizontal_tail_center_z
            + thickness_value * horizontal_tail_chord,
        )
        for x_value, thickness_value in zip(
            normalized_x,
            normalized_tail_thickness,
        )
    ]

    tail_lower_surface = [
        (
            tail_position + x_value * horizontal_tail_chord,
            horizontal_tail_center_z
            - thickness_value * horizontal_tail_chord,
        )
        for x_value, thickness_value in zip(
            reversed(normalized_x),
            reversed(normalized_tail_thickness),
        )
    ]

    horizontal_tail_side_points = (
        tail_upper_surface
        + tail_lower_surface
        + [tail_upper_surface[0]]
    )

    # Attach the vertical tail to the fuselage's sloped upper surface.
    fuselage_taper_start_x = 0.72 * fuselage_length
    fuselage_top_z = fuselage_height / 2.0


    def get_fuselage_upper_z(x_position: float) -> float:
        """Return the fuselage upper-surface height at x_position."""

        if x_position <= fuselage_taper_start_x:
            return fuselage_top_z

        if x_position >= fuselage_length:
            return 0.0

        taper_fraction = (
            fuselage_length - x_position
        ) / (
            fuselage_length - fuselage_taper_start_x
        )

        return fuselage_top_z * taper_fraction


    vertical_tail_leading_x = tail_position
    vertical_tail_trailing_x = min(
        tail_position + vertical_tail_root_chord,
        fuselage_length,
    )

    vertical_tail_front_base_z = get_fuselage_upper_z(
        vertical_tail_leading_x
    )

    vertical_tail_rear_base_z = get_fuselage_upper_z(
        vertical_tail_trailing_x
    )

    # Slight overlap prevents a visible plotting gap.
    attachment_overlap = 0.01 * fuselage_height

    vertical_tail_side_points = [
        (
            vertical_tail_leading_x,
            vertical_tail_front_base_z - attachment_overlap,
        ),
        (
            vertical_tail_trailing_x,
            vertical_tail_rear_base_z - attachment_overlap,
        ),
        (
            tail_position + vertical_tail_tip_chord,
            vertical_tail_front_base_z + vertical_tail_height,
        ),
        (
            vertical_tail_leading_x,
            vertical_tail_front_base_z + vertical_tail_height,
        ),
        (
            vertical_tail_leading_x,
            vertical_tail_front_base_z - attachment_overlap,
        ),
    ]

    return {
        "configuration": "Conventional",
        "fuselage_side_points": fuselage_side_points,
        "wing_side_points": wing_side_points,
        "horizontal_tail_side_points": (
            horizontal_tail_side_points
        ),
        "vertical_tail_side_points": (
            vertical_tail_side_points
        ),
        "boom_side_points": [],
    }

def generate_twin_boom_side_view(
    aircraft_layout: dict,
) -> dict:
    """
    Generate side-view coordinates for a twin-boom aircraft.

    The two booms overlap in a side view, so they appear as
    one boom profile. The boom connects the main wing to the
    horizontal-tail region.
    """

    fuselage_length = aircraft_layout["fuselage_length"]
    fuselage_width = aircraft_layout["fuselage_width"]

    wing_leading_edge_x = aircraft_layout[
        "wing_leading_edge_x"
    ]
    wing_root_chord = aircraft_layout["wing_root_chord"]

    horizontal_tail_points = aircraft_layout[
        "horizontal_tail_points"
    ]

    tail_position = min(
        point[0] for point in horizontal_tail_points
    )

    horizontal_tail_chord = aircraft_layout[
        "horizontal_tail_root_chord"
    ]

    vertical_tail_height = aircraft_layout[
        "vertical_tail_height"
    ]
    vertical_tail_root_chord = aircraft_layout[
        "vertical_tail_root_chord"
    ]
    vertical_tail_tip_chord = aircraft_layout[
        "vertical_tail_tip_chord"
    ]

    fuselage_height = 0.65 * fuselage_width
    wing_thickness = 0.12 * wing_root_chord
    tail_thickness = 0.10 * horizontal_tail_chord

    # Short central fuselage pod.
    pod_end_x = min(
        fuselage_length,
        wing_leading_edge_x + 1.15 * wing_root_chord,
    )

    fuselage_side_points = [
        (0.0, 0.0),
        (
            0.10 * pod_end_x,
            fuselage_height / 2.0,
        ),
        (
            0.72 * pod_end_x,
            fuselage_height / 2.0,
        ),
        (
            pod_end_x,
            0.0,
        ),
        (
            0.72 * pod_end_x,
            -fuselage_height / 2.0,
        ),
        (
            0.10 * pod_end_x,
            -fuselage_height / 2.0,
        ),
        (0.0, 0.0),
    ]

    # Smooth NACA-style main-wing root profile.
    import numpy as np

    thickness_ratio = 0.12
    number_of_points = 60

    theta = np.linspace(
        0.0,
        np.pi,
        number_of_points,
    )

    normalized_x = 0.5 * (
        1.0 - np.cos(theta)
    )

    normalized_thickness = (
        5.0
        * thickness_ratio
        * (
            0.2969 * np.sqrt(normalized_x)
            - 0.1260 * normalized_x
            - 0.3516 * normalized_x**2
            + 0.2843 * normalized_x**3
            - 0.1036 * normalized_x**4
        )
    )

    upper_surface = [
        (
            wing_leading_edge_x
            + x_value * wing_root_chord,
            thickness_value * wing_root_chord,
        )
        for x_value, thickness_value in zip(
            normalized_x,
            normalized_thickness,
        )
    ]

    lower_surface = [
        (
            wing_leading_edge_x
            + x_value * wing_root_chord,
            -thickness_value * wing_root_chord,
        )
        for x_value, thickness_value in zip(
            reversed(normalized_x),
            reversed(normalized_thickness),
        )
    ]

    wing_side_points = (
        upper_surface
        + lower_surface
        + [upper_surface[0]]
    )

    # In a side view, the left and right booms overlap.
    # Start inside the wing so there is no visible gap.
    boom_start_x = (
        wing_leading_edge_x + 0.35 * wing_root_chord
    )

    # Extend beneath the horizontal tail so they connect.
    boom_end_x = tail_position + horizontal_tail_chord

    boom_center_z = -0.05 * fuselage_height
    boom_height = max(
        0.35 * wing_thickness,
        0.25 * tail_thickness,
    )

    boom_side_points = [
        (
            boom_start_x,
            boom_center_z + boom_height / 2.0,
        ),
        (
            boom_end_x,
            boom_center_z + boom_height / 2.0,
        ),
        (
            boom_end_x,
            boom_center_z - boom_height / 2.0,
        ),
        (
            boom_start_x,
            boom_center_z - boom_height / 2.0,
        ),
        (
            boom_start_x,
            boom_center_z + boom_height / 2.0,
        ),
    ]

    # Center the horizontal tail directly on the booms.
    horizontal_tail_center_z = boom_center_z

    horizontal_tail_side_points = [
        (
            tail_position,
            horizontal_tail_center_z,
        ),
        (
            tail_position + 0.25 * horizontal_tail_chord,
            horizontal_tail_center_z + tail_thickness / 2.0,
        ),
        (
            tail_position + horizontal_tail_chord,
            horizontal_tail_center_z,
        ),
        (
            tail_position + 0.25 * horizontal_tail_chord,
            horizontal_tail_center_z - tail_thickness / 2.0,
        ),
        (
            tail_position,
            horizontal_tail_center_z,
        ),
    ]

    # Both vertical fins overlap visually in a side view.
    vertical_tail_base_z = (
        boom_center_z + boom_height / 2.0
    )

    vertical_tail_side_points = [
        (
            tail_position,
            vertical_tail_base_z,
        ),
        (
            tail_position + vertical_tail_root_chord,
            vertical_tail_base_z,
        ),
        (
            tail_position + vertical_tail_tip_chord,
            vertical_tail_base_z + vertical_tail_height,
        ),
        (
            tail_position,
            vertical_tail_base_z + vertical_tail_height,
        ),
        (
            tail_position,
            vertical_tail_base_z,
        ),
    ]

    return {
        "configuration": "Twin Boom",
        "fuselage_side_points": fuselage_side_points,
        "wing_side_points": wing_side_points,
        "horizontal_tail_side_points": (
            horizontal_tail_side_points
        ),
        "vertical_tail_side_points": (
            vertical_tail_side_points
        ),
        "boom_side_points": boom_side_points,
    }

def generate_flying_wing_side_view(
    aircraft_layout: dict,
) -> dict:
    """
    Generate a smooth airfoil-shaped side view for a flying wing.

    The center section is thicker than a conventional wing because
    it must contain the battery, payload, avionics, and structure.
    """

    import numpy as np

    wing_leading_edge_x = aircraft_layout[
        "wing_leading_edge_x"
    ]
    wing_root_chord = aircraft_layout["wing_root_chord"]

    # 14%-thick symmetric center-section airfoil.
    thickness_ratio = 0.14
    number_of_points = 60

    # Cosine spacing places more points near the leading edge.
    theta = np.linspace(
        0.0,
        np.pi,
        number_of_points,
    )

    normalized_x = 0.5 * (
        1.0 - np.cos(theta)
    )

    # NACA four-digit thickness equation.
    normalized_thickness = (
        5.0
        * thickness_ratio
        * (
            0.2969 * np.sqrt(normalized_x)
            - 0.1260 * normalized_x
            - 0.3516 * normalized_x**2
            + 0.2843 * normalized_x**3
            - 0.1036 * normalized_x**4
        )
    )

    upper_surface = [
        (
            wing_leading_edge_x
            + x_value * wing_root_chord,
            thickness_value * wing_root_chord,
        )
        for x_value, thickness_value in zip(
            normalized_x,
            normalized_thickness,
        )
    ]

    lower_surface = [
        (
            wing_leading_edge_x
            + x_value * wing_root_chord,
            -thickness_value * wing_root_chord,
        )
        for x_value, thickness_value in zip(
            reversed(normalized_x),
            reversed(normalized_thickness),
        )
    ]

    wing_side_points = (
        upper_surface
        + lower_surface
        + [upper_surface[0]]
    )

    return {
        "configuration": "Flying Wing",
        "fuselage_side_points": [],
        "wing_side_points": wing_side_points,
        "horizontal_tail_side_points": [],
        "vertical_tail_side_points": [],
        "boom_side_points": [],
    }

def generate_configuration_side_view(
    configuration_name: str,
    aircraft_layout: dict,
) -> dict:
    """
    Select and generate the correct side-view geometry
    for the chosen aircraft configuration.
    """

    normalized_name = (
        configuration_name
        .strip()
        .lower()
        .replace("-", " ")
        .replace("_", " ")
    )

    if normalized_name == "conventional":
        return generate_conventional_side_view(
            aircraft_layout
        )

    if normalized_name == "twin boom":
        return generate_twin_boom_side_view(
            aircraft_layout
        )

    if normalized_name == "flying wing":
        return generate_flying_wing_side_view(
            aircraft_layout
        )

    raise ValueError(
        "Unsupported aircraft configuration: "
        f"{configuration_name}"
    )


def plot_aircraft_layout(aircraft_layout: dict) -> None:
    """Plot a complete aircraft layout from above."""

    import matplotlib.pyplot as plt

    configuration = aircraft_layout["configuration"]
    wing_geometry = aircraft_layout["wing_geometry"]
    wing_leading_edge_x = aircraft_layout["wing_leading_edge_x"]

    center_le = wing_geometry["center_le"]
    center_te = wing_geometry["center_te"]
    right_tip_le = wing_geometry["right_tip_le"]
    right_tip_te = wing_geometry["right_tip_te"]
    left_tip_le = wing_geometry["left_tip_le"]
    left_tip_te = wing_geometry["left_tip_te"]

    wing_x = [
        left_tip_le[0] + wing_leading_edge_x,
        center_le[0] + wing_leading_edge_x,
        right_tip_le[0] + wing_leading_edge_x,
        right_tip_te[0] + wing_leading_edge_x,
        center_te[0] + wing_leading_edge_x,
        left_tip_te[0] + wing_leading_edge_x,
        left_tip_le[0] + wing_leading_edge_x,
    ]

    wing_y = [
        left_tip_le[1],
        center_le[1],
        right_tip_le[1],
        right_tip_te[1],
        center_te[1],
        left_tip_te[1],
        left_tip_le[1],
    ]

    plt.figure(figsize=(12, 7))

    plt.fill(
        wing_x,
        wing_y,
        alpha=0.35,
        label="Main Wing",
    )

    plt.plot(
        wing_x,
        wing_y,
        marker="o",
        linewidth=2,
    )

    fuselage_points = aircraft_layout["fuselage_points"]

    if fuselage_points:
        fuselage_x = [
            point[0] for point in fuselage_points
        ]
        fuselage_y = [
            point[1] for point in fuselage_points
        ]

        plt.fill(
            fuselage_x,
            fuselage_y,
            alpha=0.45,
            label="Fuselage",
        )

        plt.plot(
            fuselage_x,
            fuselage_y,
            linewidth=2,
        )

    tail_points = aircraft_layout["horizontal_tail_points"]

    if tail_points:
        tail_x = [
            point[0] for point in tail_points
        ]
        tail_y = [
            point[1] for point in tail_points
        ]

        plt.fill(
            tail_x,
            tail_y,
            alpha=0.35,
            label="Horizontal Tail",
        )

        plt.plot(
            tail_x,
            tail_y,
            marker="o",
            linewidth=2,
        )

    left_boom_points = aircraft_layout.get(
        "left_boom_points",
        [],
    )
    right_boom_points = aircraft_layout.get(
        "right_boom_points",
        [],
    )

    for boom_number, boom_points in enumerate(
        [left_boom_points, right_boom_points],
        start=1,
    ):
        if boom_points:
            boom_x = [
                point[0] for point in boom_points
            ]
            boom_y = [
                point[1] for point in boom_points
            ]

            plt.fill(
                boom_x,
                boom_y,
                alpha=0.45,
                label=(
                    "Twin Booms"
                    if boom_number == 1
                    else None
                ),
            )

            plt.plot(
                boom_x,
                boom_y,
                linewidth=2,
            )
    
    plt.axhline(
        y=0.0,
        linestyle="--",
        linewidth=1,
    )

    plt.xlabel("Longitudinal Position, x (m)")
    plt.ylabel("Spanwise Position, y (m)")
    plt.title(
        f"Generated {configuration} Aircraft — Top View"
    )

    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()



def plot_aircraft_side_view(
    side_view_geometry: dict,
) -> None:
    """
    Plot the side view of the selected aircraft configuration.
    """

    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    configuration = side_view_geometry["configuration"]

    component_styles = [
        (
            "fuselage_side_points",
            "Fuselage",
            "lightgray",
            "black",
            3,
        ),
        (
            "boom_side_points",
            "Tail Boom",
            "dimgray",
            "black",
            2,
        ),
        (
            "wing_side_points",
            "Main Wing",
            "cornflowerblue",
            "navy",
            4,
        ),
        (
            "horizontal_tail_side_points",
            "Horizontal Tail",
            "lightskyblue",
            "navy",
            4,
        ),
        (
            "vertical_tail_side_points",
            "Vertical Tail",
            "royalblue",
            "navy",
            5,
        ),
    ]

    fig, ax = plt.subplots(figsize=(12, 5))

    all_x_coordinates = []
    all_z_coordinates = []

    for (
        dictionary_key,
        label,
        face_color,
        edge_color,
        layer_order,
    ) in component_styles:

        points = side_view_geometry.get(
            dictionary_key,
            [],
        )

        # Flying-wing and other configurations can intentionally
        # omit components, so empty lists are skipped safely.
        if not points:
            continue

        polygon = Polygon(
            points,
            closed=True,
            facecolor=face_color,
            edgecolor=edge_color,
            linewidth=1.8,
            alpha=0.85,
            label=label,
            zorder=layer_order,
        )

        ax.add_patch(polygon)

        all_x_coordinates.extend(
            point[0] for point in points
        )
        all_z_coordinates.extend(
            point[1] for point in points
        )

    if not all_x_coordinates:
        raise ValueError(
            "The side-view geometry contains no drawable points."
        )

    minimum_x = min(all_x_coordinates)
    maximum_x = max(all_x_coordinates)
    minimum_z = min(all_z_coordinates)
    maximum_z = max(all_z_coordinates)

    x_range = max(maximum_x - minimum_x, 0.1)
    z_range = max(maximum_z - minimum_z, 0.1)

    ax.set_xlim(
        minimum_x - 0.08 * x_range,
        maximum_x + 0.08 * x_range,
    )

    ax.set_ylim(
        minimum_z - 0.25 * z_range,
        maximum_z + 0.25 * z_range,
    )

    ax.axhline(
        y=0.0,
        color="gray",
        linestyle="--",
        linewidth=0.8,
        alpha=0.6,
    )

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Longitudinal Position, x (m)")
    ax.set_ylabel("Vertical Position, z (m)")
    ax.set_title(
        f"{configuration} Aircraft — Side View"
    )
    ax.grid(
        True,
        linestyle=":",
        linewidth=0.7,
        alpha=0.6,
    )
    ax.legend(loc="upper right")

    plt.tight_layout()
    plt.show()