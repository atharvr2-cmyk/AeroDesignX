"""Create interactive 3D visualizations of aircraft configurations."""

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def add_main_wing(
    axes,
    aircraft_layout: dict,
) -> None:
    """Add the main wing as a thin three-dimensional solid."""

    wing_geometry = aircraft_layout["wing_geometry"]
    wing_leading_edge_x = aircraft_layout[
        "wing_leading_edge_x"
    ]

    wing_thickness = (
        0.08 * aircraft_layout["wing_root_chord"]
    )

    def shift_point(point, vertical_offset):
        """Move a wing coordinate into the aircraft reference frame."""

        return (
            point[0] + wing_leading_edge_x,
            point[1],
            point[2] + vertical_offset,
        )

    center_le = wing_geometry["center_le"]
    center_te = wing_geometry["center_te"]
    right_tip_le = wing_geometry["right_tip_le"]
    right_tip_te = wing_geometry["right_tip_te"]
    left_tip_le = wing_geometry["left_tip_le"]
    left_tip_te = wing_geometry["left_tip_te"]

    upper_offset = wing_thickness / 2.0
    lower_offset = -wing_thickness / 2.0

    upper_center_le = shift_point(center_le, upper_offset)
    upper_center_te = shift_point(center_te, upper_offset)
    upper_right_tip_le = shift_point(
        right_tip_le,
        upper_offset,
    )
    upper_right_tip_te = shift_point(
        right_tip_te,
        upper_offset,
    )
    upper_left_tip_le = shift_point(
        left_tip_le,
        upper_offset,
    )
    upper_left_tip_te = shift_point(
        left_tip_te,
        upper_offset,
    )

    lower_center_le = shift_point(center_le, lower_offset)
    lower_center_te = shift_point(center_te, lower_offset)
    lower_right_tip_le = shift_point(
        right_tip_le,
        lower_offset,
    )
    lower_right_tip_te = shift_point(
        right_tip_te,
        lower_offset,
    )
    lower_left_tip_le = shift_point(
        left_tip_le,
        lower_offset,
    )
    lower_left_tip_te = shift_point(
        left_tip_te,
        lower_offset,
    )

    wing_faces = [
        # Upper surfaces
        [
            upper_center_le,
            upper_right_tip_le,
            upper_right_tip_te,
            upper_center_te,
        ],
        [
            upper_center_le,
            upper_left_tip_le,
            upper_left_tip_te,
            upper_center_te,
        ],

        # Lower surfaces
        [
            lower_center_le,
            lower_center_te,
            lower_right_tip_te,
            lower_right_tip_le,
        ],
        [
            lower_center_le,
            lower_center_te,
            lower_left_tip_te,
            lower_left_tip_le,
        ],

        # Leading edges
        [
            upper_center_le,
            lower_center_le,
            lower_right_tip_le,
            upper_right_tip_le,
        ],
        [
            upper_center_le,
            lower_center_le,
            lower_left_tip_le,
            upper_left_tip_le,
        ],

        # Trailing edges
        [
            upper_center_te,
            upper_right_tip_te,
            lower_right_tip_te,
            lower_center_te,
        ],
        [
            upper_center_te,
            upper_left_tip_te,
            lower_left_tip_te,
            lower_center_te,
        ],

        # Wing tips
        [
            upper_right_tip_le,
            lower_right_tip_le,
            lower_right_tip_te,
            upper_right_tip_te,
        ],
        [
            upper_left_tip_le,
            lower_left_tip_le,
            lower_left_tip_te,
            upper_left_tip_te,
        ],
    ]

    wing_surface = Poly3DCollection(
        wing_faces,
        facecolor="royalblue",
        edgecolor="navy",
        linewidth=0.9,
        alpha=0.90,
    )

    axes.add_collection3d(wing_surface)

def add_fuselage(
    axes,
    aircraft_layout: dict,
) -> None:
    """
    Add a simplified three-dimensional fuselage.

    The top-view fuselage outline is extended vertically to
    create a closed 3D body.
    """

    fuselage_points = aircraft_layout["fuselage_points"]

    # Flying wings do not have a separate fuselage.
    if not fuselage_points:
        return

    fuselage_width = aircraft_layout["fuselage_width"]
    fuselage_height = 0.65 * fuselage_width

    upper_points = [
        (x, y, fuselage_height / 2.0)
        for x, y in fuselage_points
    ]

    lower_points = [
        (x, y, -fuselage_height / 2.0)
        for x, y in fuselage_points
    ]

    fuselage_faces = [
        upper_points,
        list(reversed(lower_points)),
    ]

    number_of_points = len(fuselage_points)

    for index in range(number_of_points):
        next_index = (index + 1) % number_of_points

        side_face = [
            upper_points[index],
            upper_points[next_index],
            lower_points[next_index],
            lower_points[index],
        ]

        fuselage_faces.append(side_face)

    fuselage_surface = Poly3DCollection(
        fuselage_faces,
        facecolor="lightgray",
        edgecolor="dimgray",
        linewidth=1.0,
        alpha=0.95,
    )

    axes.add_collection3d(fuselage_surface)  

def add_horizontal_tail(
    axes,
    aircraft_layout: dict,
) -> None:
    """Add the horizontal tail surface to the 3D model."""

    horizontal_tail_points = aircraft_layout[
        "horizontal_tail_points"
    ]

    if not horizontal_tail_points:
        return

    configuration = aircraft_layout["configuration"]

    if configuration == "Conventional":
        tail_z = (
            0.65
            * aircraft_layout["fuselage_width"]
            / 2.0
        )
    else:
        tail_z = 0.0

    horizontal_tail_3d = [
        (x, y, tail_z)
        for x, y in horizontal_tail_points
    ]

    horizontal_tail_surface = Poly3DCollection(
        [horizontal_tail_3d],
        facecolor="cornflowerblue",
        edgecolor="navy",
        linewidth=1.0,
        alpha=0.90,
    )

    axes.add_collection3d(horizontal_tail_surface)


def add_vertical_tails(
    axes,
    aircraft_layout: dict,
) -> None:
    """Add the vertical tail surfaces to the 3D model."""

    configuration = aircraft_layout["configuration"]

    if configuration == "Flying Wing":
        return

    vertical_tail_faces = []

    if configuration == "Conventional":
        vertical_tail_points = aircraft_layout[
            "vertical_tail_points"
        ]

        fuselage_height = (
            0.65 * aircraft_layout["fuselage_width"]
        )

        vertical_tail_face = [
            (
                x,
                0.0,
                z + fuselage_height / 2.0,
            )
            for x, z in vertical_tail_points
        ]

        vertical_tail_faces.append(
            vertical_tail_face
        )

    elif configuration == "Twin Boom":
        horizontal_tail_points = aircraft_layout[
            "horizontal_tail_points"
        ]

        tail_leading_edge_x = min(
            point[0]
            for point in horizontal_tail_points
        )

        vertical_tail_height = aircraft_layout[
            "vertical_tail_height"
        ]

        vertical_tail_root_chord = aircraft_layout[
            "vertical_tail_root_chord"
        ]

        vertical_tail_tip_chord = aircraft_layout[
            "vertical_tail_tip_chord"
        ]

        left_boom_points = aircraft_layout[
            "left_boom_points"
        ]

        right_boom_points = aircraft_layout[
            "right_boom_points"
        ]

        boom_locations = [
            sum(point[1] for point in left_boom_points[:-1])
            / len(left_boom_points[:-1]),

            sum(point[1] for point in right_boom_points[:-1])
            / len(right_boom_points[:-1]),
        ]

        for boom_y in boom_locations:
            vertical_tail_face = [
                (
                    tail_leading_edge_x,
                    boom_y,
                    0.0,
                ),
                (
                    tail_leading_edge_x
                    + vertical_tail_root_chord,
                    boom_y,
                    0.0,
                ),
                (
                    tail_leading_edge_x
                    + vertical_tail_tip_chord,
                    boom_y,
                    vertical_tail_height,
                ),
                (
                    tail_leading_edge_x,
                    boom_y,
                    vertical_tail_height,
                ),
            ]

            vertical_tail_faces.append(
                vertical_tail_face
            )

    vertical_tail_collection = Poly3DCollection(
        vertical_tail_faces,
        facecolor="slategray",
        edgecolor="black",
        linewidth=1.0,
        alpha=0.95,
    )

    axes.add_collection3d(
        vertical_tail_collection
    )

def add_booms(
    axes,
    aircraft_layout: dict,
) -> None:
    """Add the twin-boom structures to the 3D model."""

    left_boom_points = aircraft_layout.get(
        "left_boom_points",
        [],
    )

    right_boom_points = aircraft_layout.get(
        "right_boom_points",
        [],
    )

    if not left_boom_points and not right_boom_points:
        return

    boom_height = (
        0.18 * aircraft_layout["fuselage_width"]
    )

    boom_faces = []

    for boom_points in [
        left_boom_points,
        right_boom_points,
    ]:
        if not boom_points:
            continue

        upper_points = [
            (x, y, boom_height / 2.0)
            for x, y in boom_points
        ]

        lower_points = [
            (x, y, -boom_height / 2.0)
            for x, y in boom_points
        ]

        boom_faces.append(upper_points)
        boom_faces.append(
            list(reversed(lower_points))
        )

        for index in range(len(boom_points) - 1):
            boom_faces.append(
                [
                    upper_points[index],
                    upper_points[index + 1],
                    lower_points[index + 1],
                    lower_points[index],
                ]
            )

    boom_collection = Poly3DCollection(
        boom_faces,
        facecolor="silver",
        edgecolor="dimgray",
        linewidth=1.0,
        alpha=0.95,
    )

    axes.add_collection3d(boom_collection)


def plot_aircraft_3d(
    aircraft_layout: dict,
) -> None:
    """
    Display an interactive 3D aircraft visualization.

    The plot can be rotated by clicking and dragging it.
    """

    figure = plt.figure(figsize=(11, 7))
    axes = figure.add_subplot(
        111,
        projection="3d",
    )

    add_main_wing(
        axes=axes,
        aircraft_layout=aircraft_layout,
    )

    add_fuselage(
        axes=axes,
        aircraft_layout=aircraft_layout,
    )

    add_horizontal_tail(
        axes=axes,
        aircraft_layout=aircraft_layout,
    )

    add_vertical_tails(
        axes=axes,
        aircraft_layout=aircraft_layout,
    )

    add_booms(
        axes=axes,
        aircraft_layout=aircraft_layout,
    )

    wing_geometry = aircraft_layout["wing_geometry"]
    span = wing_geometry["span"]
    fuselage_length = aircraft_layout["fuselage_length"]
    wing_root_chord = aircraft_layout["wing_root_chord"]

    maximum_length = max(
        fuselage_length,
        wing_root_chord,
    )

    axes.set_xlim(
        -0.10 * maximum_length,
        1.10 * maximum_length,
    )

    axes.set_ylim(
        -0.60 * span,
        0.60 * span,
    )

    axes.set_zlim(
        -0.25 * span,
        0.25 * span,
    )

    axes.set_xlabel("Longitudinal Position, x (m)")
    axes.set_ylabel("Spanwise Position, y (m)")
    axes.set_zlabel("Vertical Position, z (m)")

    configuration = aircraft_layout["configuration"]

    axes.set_title(
        f"Generated {configuration} Aircraft — 3D View"
    )

    axes.set_box_aspect(
        (
            maximum_length,
            span,
            0.50 * span,
        )
    )

    axes.view_init(
        elev=24,
        azim=-58,
    )

    plt.tight_layout()
    plt.show()