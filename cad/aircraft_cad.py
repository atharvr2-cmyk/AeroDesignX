"""Generate parametric AeroDesignX aircraft CAD models."""

from math import cos, pi, sin, tan

import cadquery as cq
from ocp_vscode import show

from pathlib import Path

def meters_to_millimeters(value_m: float) -> float:
    """Convert an AeroDesignX dimension from meters to millimeters."""

    return value_m * 1000.0

def generate_naca_4_digit_points(
    chord_mm: float,
    thickness_ratio: float = 0.12,
    point_count: int = 50,
) -> list[tuple[float, float]]:
    """Generate a closed, symmetric NACA airfoil profile."""

    upper_points = []
    lower_points = []

    for index in range(point_count):
        angle = pi * index / (point_count - 1)

        normalized_x = 0.5 * (1.0 - cos(angle))

        thickness = (
            5.0
            * thickness_ratio
            * (
                0.2969 * normalized_x**0.5
                - 0.1260 * normalized_x
                - 0.3516 * normalized_x**2
                + 0.2843 * normalized_x**3
                - 0.1036 * normalized_x**4
            )
        )

        x_coordinate = normalized_x * chord_mm
        upper_z = thickness * chord_mm
        lower_z = -thickness * chord_mm

        upper_points.append(
            (x_coordinate, upper_z)
        )

        lower_points.append(
            (x_coordinate, lower_z)
        )

    airfoil_points = (
        upper_points
        + list(reversed(lower_points[1:-1]))
    )

    return airfoil_points

def create_half_wing(
    semi_span_mm: float,
    root_chord_mm: float,
    tip_chord_mm: float,
    sweep_mm: float = 0.0,
    dihedral_deg: float = 0.0,
    side: int = 1,
) -> cq.Shape:
    """Create a smooth tapered half-wing with a rounded wingtip."""

    section_fractions = [
        0.00,
        0.40,
        0.78,
        1.00,
    ]

    tip_shape_scales = [
        1.00,
        1.00,
        1.00,
        1.00,
    ]

    section_wires = []

    for fraction, tip_scale in zip(
        section_fractions,
        tip_shape_scales,
    ):
        y_position = side * fraction * semi_span_mm

        z_position = (
            fraction
            * semi_span_mm
            * sin(dihedral_deg * pi / 180.0)
        )

        nominal_chord_mm = (
            root_chord_mm
            + fraction * (tip_chord_mm - root_chord_mm)
        )

        chord_mm = nominal_chord_mm * tip_scale

        # Keep the shrinking tip sections centered around
        # the nominal local chord.
        x_position = (
            fraction * sweep_mm
            + 0.5 * nominal_chord_mm * (1.0 - tip_scale)
        )

        thickness_ratio = (
            0.12
            - 0.025 * fraction
        )

        airfoil_points = generate_naca_4_digit_points(
            chord_mm=chord_mm,
            thickness_ratio=thickness_ratio,
            point_count=70,
        )

        section_plane = cq.Plane(
            origin=(
                x_position,
                y_position,
                z_position,
            ),
            xDir=(1.0, 0.0, 0.0),
            normal=(0.0, side, 0.0),
        )

        section_wire = (
            cq.Workplane(section_plane)
            .spline(airfoil_points)
            .close()
            .val()
        )

        section_wires.append(section_wire)

    half_wing = cq.Solid.makeLoft(
        section_wires,
        ruled=False,
    )

    return half_wing


def create_complete_wing(
    span_mm: float,
    root_chord_mm: float,
    tip_chord_mm: float,
    sweep_mm: float = 0.0,
    dihedral_deg: float = 0.0,
) -> cq.Shape:
    """Create a complete tapered wing from two airfoil lofts."""

    semi_span_mm = span_mm / 2.0

    right_wing = create_half_wing(
        semi_span_mm=semi_span_mm,
        root_chord_mm=root_chord_mm,
        tip_chord_mm=tip_chord_mm,
        sweep_mm=sweep_mm,
        dihedral_deg=dihedral_deg,
        side=1,
    )

    left_wing = create_half_wing(
        semi_span_mm=semi_span_mm,
        root_chord_mm=root_chord_mm,
        tip_chord_mm=tip_chord_mm,
        sweep_mm=sweep_mm,
        dihedral_deg=dihedral_deg,
        side=-1,
    )

    complete_wing = right_wing.fuse(left_wing)

    return complete_wing

def create_streamlined_fuselage(
    length_mm: float,
    width_mm: float,
    height_mm: float,
    wing_leading_edge_x_mm: float = 0.0,
) -> cq.Shape:
    """Create a streamlined fuselage using elliptical loft sections."""

    nose_x = wing_leading_edge_x_mm - 0.30 * length_mm
    tail_x = nose_x + length_mm

    section_data = [
        (
            nose_x,
            0.08 * width_mm,
            0.08 * height_mm,
        ),
        (
            nose_x + 0.08 * length_mm,
            0.65 * width_mm,
            0.65 * height_mm,
        ),
        (
            nose_x + 0.22 * length_mm,
            width_mm,
            height_mm,
        ),
        (
            nose_x + 0.48 * length_mm,
            0.92 * width_mm,
            0.88 * height_mm,
        ),
        (
            nose_x + 0.78 * length_mm,
            0.52 * width_mm,
            0.48 * height_mm,
        ),
        (
            tail_x,
            0.10 * width_mm,
            0.10 * height_mm,
        ),
    ]

    fuselage_wires = []

    for x_position, section_width, section_height in section_data:
        section_plane = cq.Plane(
            origin=(x_position, 0.0, 0.0),
            xDir=(0.0, 1.0, 0.0),
            normal=(1.0, 0.0, 0.0),
        )

        section_wire = (
            cq.Workplane(section_plane)
            .ellipse(
                section_width / 2.0,
                section_height / 2.0,
            )
            .val()
        )

        fuselage_wires.append(section_wire)

    fuselage = cq.Solid.makeLoft(
        fuselage_wires,
        ruled=False,
    )

    return fuselage


def create_conventional_control_surface_gaps(
    tail_leading_edge_x_mm: float,
    horizontal_tail_span_mm: float,
    horizontal_tail_root_mm: float,
    horizontal_tail_tip_mm: float,
    horizontal_tail_sweep_mm: float,
    vertical_tail_height_mm: float,
    vertical_tail_root_mm: float,
    vertical_tail_tip_mm: float,
    vertical_tail_sweep_mm: float,
    horizontal_tail_z_mm: float,
    root_chord_mm: float,
) -> cq.Shape:
    """Create real recessed hinge slots for elevators and rudder."""

    gap_width_mm = max(
        1.0,
        0.005 * root_chord_mm,
    )

    cutter_depth_mm = max(
        8.0,
        0.05 * root_chord_mm,
    )

    half_gap_mm = gap_width_mm / 2.0

    # ---------------------------------------------------------
    # Elevator hinge slots
    # ---------------------------------------------------------

    semi_tail_span_mm = horizontal_tail_span_mm / 2.0

    elevator_inner_fraction = 0.14
    elevator_outer_fraction = 0.90
    elevator_hinge_fraction = 0.74

    inner_y_mm = (
        elevator_inner_fraction
        * semi_tail_span_mm
    )

    outer_y_mm = (
        elevator_outer_fraction
        * semi_tail_span_mm
    )

    inner_chord_mm = (
        horizontal_tail_root_mm
        + elevator_inner_fraction
        * (
            horizontal_tail_tip_mm
            - horizontal_tail_root_mm
        )
    )

    outer_chord_mm = (
        horizontal_tail_root_mm
        + elevator_outer_fraction
        * (
            horizontal_tail_tip_mm
            - horizontal_tail_root_mm
        )
    )

    inner_hinge_x_mm = (
        tail_leading_edge_x_mm
        + elevator_inner_fraction
        * horizontal_tail_sweep_mm
        + elevator_hinge_fraction * inner_chord_mm
    )

    outer_hinge_x_mm = (
        tail_leading_edge_x_mm
        + elevator_outer_fraction
        * horizontal_tail_sweep_mm
        + elevator_hinge_fraction * outer_chord_mm
    )

    right_elevator_gap = (
        cq.Workplane(
            "XY",
            origin=(0.0, 0.0, horizontal_tail_z_mm),
        )
        .polyline(
            [
                (
                    inner_hinge_x_mm - half_gap_mm,
                    inner_y_mm,
                ),
                (
                    outer_hinge_x_mm - half_gap_mm,
                    outer_y_mm,
                ),
                (
                    outer_hinge_x_mm + half_gap_mm,
                    outer_y_mm,
                ),
                (
                    inner_hinge_x_mm + half_gap_mm,
                    inner_y_mm,
                ),
            ]
        )
        .close()
        .extrude(
            cutter_depth_mm,
            both=True,
        )
        .val()
    )

    left_elevator_gap = (
        cq.Workplane(
            "XY",
            origin=(0.0, 0.0, horizontal_tail_z_mm),
        )
        .polyline(
            [
                (
                    inner_hinge_x_mm - half_gap_mm,
                    -inner_y_mm,
                ),
                (
                    outer_hinge_x_mm - half_gap_mm,
                    -outer_y_mm,
                ),
                (
                    outer_hinge_x_mm + half_gap_mm,
                    -outer_y_mm,
                ),
                (
                    inner_hinge_x_mm + half_gap_mm,
                    -inner_y_mm,
                ),
            ]
        )
        .close()
        .extrude(
            cutter_depth_mm,
            both=True,
        )
        .val()
    )

    # ---------------------------------------------------------
    # Rudder hinge slot
    # ---------------------------------------------------------

    rudder_lower_fraction = 0.12
    rudder_upper_fraction = 0.88
    rudder_hinge_fraction = 0.72

    lower_z_mm = (
        rudder_lower_fraction
        * vertical_tail_height_mm
    )

    upper_z_mm = (
        rudder_upper_fraction
        * vertical_tail_height_mm
    )

    lower_chord_mm = (
        vertical_tail_root_mm
        + rudder_lower_fraction
        * (
            vertical_tail_tip_mm
            - vertical_tail_root_mm
        )
    )

    upper_chord_mm = (
        vertical_tail_root_mm
        + rudder_upper_fraction
        * (
            vertical_tail_tip_mm
            - vertical_tail_root_mm
        )
    )

    lower_hinge_x_mm = (
        tail_leading_edge_x_mm
        + rudder_lower_fraction
        * vertical_tail_sweep_mm
        + rudder_hinge_fraction * lower_chord_mm
    )

    upper_hinge_x_mm = (
        tail_leading_edge_x_mm
        + rudder_upper_fraction
        * vertical_tail_sweep_mm
        + rudder_hinge_fraction * upper_chord_mm
    )

    rudder_gap = (
        cq.Workplane("XZ")
        .polyline(
            [
                (
                    lower_hinge_x_mm - half_gap_mm,
                    lower_z_mm,
                ),
                (
                    upper_hinge_x_mm - half_gap_mm,
                    upper_z_mm,
                ),
                (
                    upper_hinge_x_mm + half_gap_mm,
                    upper_z_mm,
                ),
                (
                    lower_hinge_x_mm + half_gap_mm,
                    lower_z_mm,
                ),
            ]
        )
        .close()
        .extrude(
            cutter_depth_mm,
            both=True,
        )
        .val()
    )

    return (
        right_elevator_gap
        .fuse(left_elevator_gap)
        .fuse(rudder_gap)
    )

def create_conventional_wing_root_fairings(
    fuselage_width_mm: float,
    root_chord_mm: float,
) -> cq.Shape:
    """Create smooth fairings at the conventional wing roots."""

    fairing_length_mm = 0.88 * root_chord_mm
    fairing_width_mm = 0.26 * root_chord_mm
    fairing_height_mm = 0.055 * root_chord_mm

    fairing_start_x_mm = 0.04 * root_chord_mm

    fairings = []

    for side in (-1, 1):
        center_y_mm = side * (
            0.50 * fuselage_width_mm
            + 0.04 * fairing_width_mm
        )

        section_data = [
            (0.00, 0.20, 0.25),
            (0.12, 0.75, 0.70),
            (0.38, 1.00, 1.00),
            (0.72, 0.72, 0.65),
            (1.00, 0.18, 0.22),
        ]

        section_wires = []

        for (
            length_fraction,
            width_scale,
            height_scale,
        ) in section_data:
            x_position_mm = (
                fairing_start_x_mm
                + length_fraction * fairing_length_mm
            )

            section_plane = cq.Plane(
                origin=(
                    x_position_mm,
                    center_y_mm,
                    0.0,
                ),
                xDir=(0.0, 1.0, 0.0),
                normal=(1.0, 0.0, 0.0),
            )

            section_wire = (
                cq.Workplane(section_plane)
                .ellipse(
                    0.5 * fairing_width_mm * width_scale,
                    0.5 * fairing_height_mm * height_scale,
                )
                .val()
            )

            section_wires.append(section_wire)

        fairing = cq.Solid.makeLoft(
            section_wires,
            ruled=False,
        )

        fairings.append(fairing)

    return fairings[0].fuse(fairings[1])


def create_conventional_aircraft(
    wing_geometry: dict,
    component_sizes: dict,
) -> cq.Shape:
    """Create a conventional aircraft using AeroDesignX sizing results."""

    span_mm = meters_to_millimeters(
        wing_geometry["span"]
    )
    root_chord_mm = meters_to_millimeters(
        wing_geometry["root_chord"]
    )
    tip_chord_mm = meters_to_millimeters(
        wing_geometry["tip_chord"]
    )

    sweep_deg = wing_geometry.get("sweep", 0.0)
    dihedral_deg = wing_geometry.get("dihedral", 0.0)

    # Convert sweep angle into the tip's rearward displacement.
    sweep_mm = (
        span_mm
        / 2.0
        * tan(sweep_deg * pi / 180.0)
    )

    raw_fuselage_length_mm = meters_to_millimeters(
        component_sizes["fuselage_length"]
    )
    raw_fuselage_width_mm = meters_to_millimeters(
        component_sizes["fuselage_width"]
    )

    # Keep the optimized dimensions, but constrain them to
    # believable proportions for a conventional fixed-wing UAV.
    fuselage_length_mm = min(
        raw_fuselage_length_mm,
        0.60 * span_mm,
    )
    fuselage_length_mm = max(
        fuselage_length_mm,
        3.20 * root_chord_mm,
    )

    fuselage_width_mm = max(
        raw_fuselage_width_mm,
        0.48 * root_chord_mm,
    )
    fuselage_width_mm = min(
        fuselage_width_mm,
        0.16 * fuselage_length_mm,
    )

    main_wing = create_complete_wing(
        span_mm=span_mm,
        root_chord_mm=root_chord_mm,
        tip_chord_mm=tip_chord_mm,
        sweep_mm=sweep_mm,
        dihedral_deg=dihedral_deg,
    )

    fuselage = create_streamlined_fuselage(
        length_mm=fuselage_length_mm,
        width_mm=fuselage_width_mm,
        height_mm=1.05 * fuselage_width_mm,
        wing_leading_edge_x_mm=0.0,
    )

    wing_root_fairings = (
        create_conventional_wing_root_fairings(
            fuselage_width_mm=fuselage_width_mm,
            root_chord_mm=root_chord_mm,
        )
    )

    horizontal_tail_span_mm = meters_to_millimeters(
        component_sizes["horizontal_tail_span"]
    )
    horizontal_tail_root_mm = meters_to_millimeters(
        component_sizes["horizontal_tail_root_chord"]
    )
    horizontal_tail_tip_mm = meters_to_millimeters(
        component_sizes["horizontal_tail_tip_chord"]
    )

    vertical_tail_height_mm = meters_to_millimeters(
        component_sizes["vertical_tail_height"]
    )
    vertical_tail_root_mm = meters_to_millimeters(
        component_sizes["vertical_tail_root_chord"]
    )
    vertical_tail_tip_mm = meters_to_millimeters(
        component_sizes["vertical_tail_tip_chord"]
    )

        # Refine the horizontal-tail proportions.
    horizontal_tail_tip_mm = max(
        horizontal_tail_tip_mm,
        0.48 * horizontal_tail_root_mm,
    )
    horizontal_tail_tip_mm = min(
        horizontal_tail_tip_mm,
        0.62 * horizontal_tail_root_mm,
    )

    # Make the vertical stabilizer more prominent and tapered.
    vertical_tail_height_mm = max(
        vertical_tail_height_mm,
        0.34 * horizontal_tail_span_mm,
    )

    vertical_tail_root_mm = max(
        vertical_tail_root_mm,
        0.90 * horizontal_tail_root_mm,
    )

    vertical_tail_tip_mm = max(
        vertical_tail_tip_mm,
        0.32 * vertical_tail_root_mm,
    )
    vertical_tail_tip_mm = min(
        vertical_tail_tip_mm,
        0.48 * vertical_tail_root_mm,
    )

    # The fuselage ends at 70% of its length because its nose
    # begins 30% of the length ahead of the main wing.
    fuselage_tail_x_mm = 0.70 * fuselage_length_mm

    # Position the stabilizers far enough forward to overlap
    # the rear fuselage and remain one connected solid.
    tail_leading_edge_x_mm = (
        fuselage_tail_x_mm
        - 0.88 * horizontal_tail_root_mm
    )

    horizontal_tail_sweep_mm = (
        0.28 * horizontal_tail_root_mm
    )

    horizontal_tail_z_mm = (
        0.06 * fuselage_width_mm
    )

    horizontal_tail = create_complete_wing(
        span_mm=horizontal_tail_span_mm,
        root_chord_mm=horizontal_tail_root_mm,
        tip_chord_mm=horizontal_tail_tip_mm,
        sweep_mm=horizontal_tail_sweep_mm,
        dihedral_deg=0.0,
    ).translate(
        (
            tail_leading_edge_x_mm,
            0.0,
            horizontal_tail_z_mm,
        )
    )

    vertical_tail_sweep_mm = (
        0.42 * vertical_tail_root_mm
    )

    vertical_tail = create_half_wing(
        semi_span_mm=vertical_tail_height_mm,
        root_chord_mm=vertical_tail_root_mm,
        tip_chord_mm=vertical_tail_tip_mm,
        sweep_mm=vertical_tail_sweep_mm,
        dihedral_deg=0.0,
        side=1,
    ).rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        90.0,
    ).translate(
        (
            tail_leading_edge_x_mm,
            0.0,
            0.0,
        )
    )

    control_surface_gaps = create_conventional_control_surface_gaps(
        tail_leading_edge_x_mm=tail_leading_edge_x_mm,
        horizontal_tail_span_mm=horizontal_tail_span_mm,
        horizontal_tail_root_mm=horizontal_tail_root_mm,
        horizontal_tail_tip_mm=horizontal_tail_tip_mm,
        horizontal_tail_sweep_mm=horizontal_tail_sweep_mm,
        vertical_tail_height_mm=vertical_tail_height_mm,
        vertical_tail_root_mm=vertical_tail_root_mm,
        vertical_tail_tip_mm=vertical_tail_tip_mm,
        vertical_tail_sweep_mm=vertical_tail_sweep_mm,
        horizontal_tail_z_mm=horizontal_tail_z_mm,
        root_chord_mm=root_chord_mm,
    )

    conventional_aircraft = (
        main_wing
        .fuse(fuselage)
        .fuse(wing_root_fairings)
        .fuse(horizontal_tail)
        .fuse(vertical_tail)
        .cut(control_surface_gaps)
    )

    return conventional_aircraft

def create_streamlined_boom(
    start_x_mm: float,
    length_mm: float,
    width_mm: float,
    height_mm: float,
    y_position_mm: float,
    z_position_mm: float = 0.0,
) -> cq.Shape:
    """Create one tapered aerodynamic tail boom."""

    section_data = [
        (start_x_mm, 0.85, 0.85),
        (start_x_mm + 0.12 * length_mm, 1.00, 1.00),
        (start_x_mm + 0.55 * length_mm, 0.72, 0.72),
        (start_x_mm + 0.88 * length_mm, 0.48, 0.48),
        (start_x_mm + length_mm, 0.40, 0.40),
    ]

    boom_wires = []

    for x_position, width_scale, height_scale in section_data:
        section_plane = cq.Plane(
            origin=(
                x_position,
                y_position_mm,
                z_position_mm,
            ),
            xDir=(0.0, 1.0, 0.0),
            normal=(1.0, 0.0, 0.0),
        )

        section_wire = (
            cq.Workplane(section_plane)
            .ellipse(
                width_mm * width_scale / 2.0,
                height_mm * height_scale / 2.0,
            )
            .val()
        )

        boom_wires.append(section_wire)

    return cq.Solid.makeLoft(
        boom_wires,
        ruled=False,
    )

def create_twin_boom_control_surface_gaps(
    tail_x_mm: float,
    boom_y_mm: float,
    boom_z_mm: float,
    horizontal_tail_root_mm: float,
    vertical_tail_height_mm: float,
    vertical_tail_root_mm: float,
) -> cq.Shape:
    """Create visible Twin Boom elevator and rudder hinge slots."""

    gap_width_mm = max(
        1.2,
        0.006 * horizontal_tail_root_mm,
    )

    cutter_depth_mm = max(
        12.0,
        0.08 * horizontal_tail_root_mm,
    )

    # Elevator hinge across the central horizontal tail.
    elevator_hinge_x_mm = (
        tail_x_mm
        + 0.73 * horizontal_tail_root_mm
    )

    elevator_gap = (
        cq.Workplane("XY")
        .box(
            gap_width_mm,
            1.76 * boom_y_mm,
            cutter_depth_mm,
            centered=(True, True, True),
        )
        .translate(
            (
                elevator_hinge_x_mm,
                0.0,
                boom_z_mm,
            )
        )
        .val()
    )

    # Rudder hinge slots on both vertical stabilizers.
    rudder_hinge_x_mm = (
        tail_x_mm
        + 0.72 * vertical_tail_root_mm
    )

    rudder_gap_height_mm = (
        0.72 * vertical_tail_height_mm
    )

    rudder_gap_center_z_mm = (
        boom_z_mm
        + 0.50 * vertical_tail_height_mm
    )

    rudder_gaps = []

    for side in (-1, 1):
        rudder_gap = (
            cq.Workplane("XZ")
            .box(
                gap_width_mm,
                rudder_gap_height_mm,
                cutter_depth_mm,
                centered=(True, True, True),
            )
            .translate(
                (
                    rudder_hinge_x_mm,
                    rudder_gap_center_z_mm,
                    side * boom_y_mm,
                )
            )
            .val()
        )

        rudder_gaps.append(rudder_gap)

    return (
        elevator_gap
        .fuse(rudder_gaps[0])
        .fuse(rudder_gaps[1])
    )


def create_twin_boom_aircraft(
    wing_geometry: dict,
    component_sizes: dict,
) -> cq.Shape:
    """Create a twin-boom UAV using AeroDesignX sizing results."""

    span_mm = meters_to_millimeters(
        wing_geometry["span"]
    )
    root_chord_mm = meters_to_millimeters(
        wing_geometry["root_chord"]
    )
    tip_chord_mm = meters_to_millimeters(
        wing_geometry["tip_chord"]
    )

    sweep_deg = wing_geometry.get("sweep", 0.0)
    dihedral_deg = wing_geometry.get("dihedral", 0.0)

    sweep_mm = (
        span_mm
        / 2.0
        * tan(sweep_deg * pi / 180.0)
    )

    fuselage_length_mm = meters_to_millimeters(
        component_sizes["fuselage_length"]
    )
    fuselage_width_mm = meters_to_millimeters(
        component_sizes["fuselage_width"]
    )

    horizontal_tail_span_mm = meters_to_millimeters(
        component_sizes["horizontal_tail_span"]
    )
    horizontal_tail_root_mm = meters_to_millimeters(
        component_sizes["horizontal_tail_root_chord"]
    )
    horizontal_tail_tip_mm = meters_to_millimeters(
        component_sizes["horizontal_tail_tip_chord"]
    )

    vertical_tail_height_mm = meters_to_millimeters(
        component_sizes["vertical_tail_height"]
    )
    vertical_tail_root_mm = meters_to_millimeters(
        component_sizes["vertical_tail_root_chord"]
    )
    vertical_tail_tip_mm = meters_to_millimeters(
        component_sizes["vertical_tail_tip_chord"]
    )

    main_wing = create_complete_wing(
        span_mm=span_mm,
        root_chord_mm=root_chord_mm,
        tip_chord_mm=tip_chord_mm,
        sweep_mm=sweep_mm,
        dihedral_deg=dihedral_deg,
    )

    # Keep the center pod compact so the twin booms—not the
    # fuselage—carry the aircraft structure toward the tail.
    center_body_length_mm = min(
        0.48 * fuselage_length_mm,
        2.60 * root_chord_mm,
    )
    center_body_length_mm = max(
        center_body_length_mm,
        2.10 * root_chord_mm,
    )

    center_body_width_mm = max(
        fuselage_width_mm,
        0.42 * root_chord_mm,
    )
    center_body_width_mm = min(
        center_body_width_mm,
        0.18 * center_body_length_mm,
    )

    center_body = create_streamlined_fuselage(
        length_mm=center_body_length_mm,
        width_mm=center_body_width_mm,
        height_mm=1.05 * center_body_width_mm,
        wing_leading_edge_x_mm=0.0,
    )

    boom_y_mm = min(
        0.23 * span_mm,
        0.45 * horizontal_tail_span_mm,
    )

    boom_start_x_mm = 0.25 * root_chord_mm
    boom_length_mm = max(
        0.65 * fuselage_length_mm,
        2.0 * root_chord_mm,
    )
    boom_z_mm = 0.06 * root_chord_mm

    boom_width_mm = 0.35 * fuselage_width_mm
    boom_height_mm = 0.42 * fuselage_width_mm

    right_boom = create_streamlined_boom(
        start_x_mm=boom_start_x_mm,
        length_mm=boom_length_mm,
        width_mm=boom_width_mm,
        height_mm=boom_height_mm,
        y_position_mm=boom_y_mm,
        z_position_mm=boom_z_mm,
    )

    left_boom = create_streamlined_boom(
        start_x_mm=boom_start_x_mm,
        length_mm=boom_length_mm,
        width_mm=boom_width_mm,
        height_mm=boom_height_mm,
        y_position_mm=-boom_y_mm,
        z_position_mm=boom_z_mm,
    )

    # Refine the twin-boom horizontal stabilizer into a broad,
    # moderately tapered tailplane instead of a pointed wing.
    # Keep only a small aerodynamic overhang outside each fin.
    horizontal_tail_span_mm = (
        2.05 * boom_y_mm
    )

    horizontal_tail_root_mm = min(
        horizontal_tail_root_mm,
        0.72 * root_chord_mm,
    )
    horizontal_tail_root_mm = max(
        horizontal_tail_root_mm,
        0.48 * root_chord_mm,
    )

    horizontal_tail_tip_mm = max(
        horizontal_tail_tip_mm,
        0.66 * horizontal_tail_root_mm,
    )
    horizontal_tail_tip_mm = min(
        horizontal_tail_tip_mm,
        0.78 * horizontal_tail_root_mm,
    )

    horizontal_tail_sweep_mm = (
        0.08 * horizontal_tail_root_mm
    )

    # Overlap the tailplane with the boom ends so all parts
    # remain attached as one connected solid.
    tail_x_mm = (
        boom_start_x_mm
        + boom_length_mm
        - 0.82 * horizontal_tail_root_mm
    )

    horizontal_tail = create_complete_wing(
        span_mm=horizontal_tail_span_mm,
        root_chord_mm=horizontal_tail_root_mm,
        tip_chord_mm=horizontal_tail_tip_mm,
        sweep_mm=horizontal_tail_sweep_mm,
        dihedral_deg=0.0,
    ).translate(
        (
            tail_x_mm,
            0.0,
            boom_z_mm,
        )
    )

    right_vertical_tail = create_half_wing(
        semi_span_mm=vertical_tail_height_mm,
        root_chord_mm=vertical_tail_root_mm,
        tip_chord_mm=vertical_tail_tip_mm,
        sweep_mm=0.30 * vertical_tail_root_mm,
        side=1,
    ).rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        90.0,
    ).translate(
        (
            tail_x_mm + 0.04 * vertical_tail_root_mm,
            boom_y_mm,
            boom_z_mm - 0.015 * vertical_tail_height_mm,
        )
    )

    left_vertical_tail = create_half_wing(
        semi_span_mm=vertical_tail_height_mm,
        root_chord_mm=vertical_tail_root_mm,
        tip_chord_mm=vertical_tail_tip_mm,
        sweep_mm=0.30 * vertical_tail_root_mm,
        side=1,
    ).rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        90.0,
    ).translate(
        (
            tail_x_mm + 0.04 * vertical_tail_root_mm,
            -boom_y_mm,
            boom_z_mm - 0.015 * vertical_tail_height_mm,
        )
    )

    control_surface_gaps = (
        create_twin_boom_control_surface_gaps(
            tail_x_mm=tail_x_mm,
            boom_y_mm=boom_y_mm,
            boom_z_mm=boom_z_mm,
            horizontal_tail_root_mm=horizontal_tail_root_mm,
            vertical_tail_height_mm=vertical_tail_height_mm,
            vertical_tail_root_mm=vertical_tail_root_mm,
        )
    )

    twin_boom_aircraft = (
        main_wing
        .fuse(center_body)
        .fuse(right_boom)
        .fuse(left_boom)
        .fuse(horizontal_tail)
        .fuse(right_vertical_tail)
        .fuse(left_vertical_tail)
    )

    return twin_boom_aircraft


def create_flying_wing_elevons(
    span_mm: float,
    root_chord_mm: float,
    tip_chord_mm: float,
    sweep_mm: float,
) -> cq.Shape:
    """Create integrated left and right flying-wing elevons."""

    semi_span_mm = span_mm / 2.0

    inner_fraction = 0.42
    outer_fraction = 0.88

    inner_y_mm = inner_fraction * semi_span_mm
    outer_y_mm = outer_fraction * semi_span_mm

    inner_chord_mm = (
        root_chord_mm
        + inner_fraction
        * (tip_chord_mm - root_chord_mm)
    )

    outer_chord_mm = (
        root_chord_mm
        + outer_fraction
        * (tip_chord_mm - root_chord_mm)
    )

    inner_leading_edge_x_mm = inner_fraction * sweep_mm
    outer_leading_edge_x_mm = outer_fraction * sweep_mm

    # Elevons occupy the rear 22% of the local wing chord.
    inner_hinge_x_mm = (
        inner_leading_edge_x_mm
        + 0.78 * inner_chord_mm
    )

    outer_hinge_x_mm = (
        outer_leading_edge_x_mm
        + 0.78 * outer_chord_mm
    )

    inner_trailing_edge_x_mm = (
        inner_leading_edge_x_mm
        + 0.96 * inner_chord_mm
    )

    outer_trailing_edge_x_mm = (
        outer_leading_edge_x_mm
        + 0.96 * outer_chord_mm
    )

    panel_thickness_mm = max(
        1.5,
        0.008 * root_chord_mm,
    )

    right_elevon = (
        cq.Workplane("XY")
        .polyline(
            [
                (inner_hinge_x_mm, inner_y_mm),
                (outer_hinge_x_mm, outer_y_mm),
                (outer_trailing_edge_x_mm, outer_y_mm),
                (inner_trailing_edge_x_mm, inner_y_mm),
            ]
        )
        .close()
        .extrude(
            panel_thickness_mm,
            both=True,
        )
    )

    left_elevon = (
        cq.Workplane("XY")
        .polyline(
            [
                (inner_hinge_x_mm, -inner_y_mm),
                (outer_hinge_x_mm, -outer_y_mm),
                (outer_trailing_edge_x_mm, -outer_y_mm),
                (inner_trailing_edge_x_mm, -inner_y_mm),
            ]
        )
        .close()
        .extrude(
            panel_thickness_mm,
            both=True,
        )
    )

    return right_elevon.val().fuse(left_elevon.val())

def create_flying_wing_aircraft(
    wing_geometry: dict,
    component_sizes: dict,
) -> cq.Shape:
    """Create a swept flying-wing UAV with a blended center body."""

    span_mm = meters_to_millimeters(
        wing_geometry["span"]
    )
    root_chord_mm = meters_to_millimeters(
        wing_geometry["root_chord"]
    )
    tip_chord_mm = meters_to_millimeters(
        wing_geometry["tip_chord"]
    )

    input_sweep_deg = wing_geometry.get("sweep", 0.0)
    dihedral_deg = wing_geometry.get("dihedral", 0.0)

    # A flying wing requires noticeable sweep to produce
    # its characteristic planform.
    flying_wing_sweep_deg = max(
        input_sweep_deg,
        22.0,
    )

    sweep_mm = (
        span_mm
        / 2.0
        * tan(flying_wing_sweep_deg * pi / 180.0)
    )

    outer_wing = create_complete_wing(
        span_mm=span_mm,
        root_chord_mm=root_chord_mm,
        tip_chord_mm=tip_chord_mm,
        sweep_mm=sweep_mm,
        dihedral_deg=dihedral_deg,
    )

    # Create a longer, narrower center body that blends
    # into the swept wing without dominating the planform.
    center_body_length_mm = 1.45 * root_chord_mm

    center_body_width_mm = min(
        0.13 * span_mm,
        0.95 * root_chord_mm,
    )

    center_body_height_mm = 0.22 * root_chord_mm

    center_body = create_streamlined_fuselage(
        length_mm=center_body_length_mm,
        width_mm=center_body_width_mm,
        height_mm=center_body_height_mm,
        wing_leading_edge_x_mm=0.16 * root_chord_mm,
    )

    elevons = create_flying_wing_elevons(
        span_mm=span_mm,
        root_chord_mm=root_chord_mm,
        tip_chord_mm=tip_chord_mm,
        sweep_mm=sweep_mm,
    )

    flying_wing = (
        outer_wing
        .fuse(center_body)
        .fuse(elevons)
    )

    return flying_wing


def generate_and_export_aircraft_cad(
    configuration_name: str,
    wing_geometry: dict,
    component_sizes: dict,
    output_directory: str = "cad/exports",
) -> cq.Shape:
    """Generate and export the selected AeroDesignX configuration."""

    normalized_name = (
        configuration_name
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )

    if normalized_name == "conventional":
        aircraft = create_conventional_aircraft(
            wing_geometry=wing_geometry,
            component_sizes=component_sizes,
        )

    elif normalized_name == "twin_boom":
        aircraft = create_twin_boom_aircraft(
            wing_geometry=wing_geometry,
            component_sizes=component_sizes,
        )

    elif normalized_name == "flying_wing":
        aircraft = create_flying_wing_aircraft(
            wing_geometry=wing_geometry,
            component_sizes=component_sizes,
        )

    else:
        raise ValueError(
            f"Unknown CAD configuration '{configuration_name}'. "
            "Available configurations: conventional, twin_boom, "
            "flying_wing."
        )

    if not aircraft.isValid():
        raise ValueError(
            f"The generated {configuration_name} CAD model is invalid."
        )

    solid_count = len(aircraft.Solids())

    if solid_count != 1:
        raise ValueError(
            f"The generated {configuration_name} model contains "
            f"{solid_count} disconnected solids."
        )

    export_folder = Path(output_directory)
    export_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_stem = f"{normalized_name}_aircraft"

    step_path = export_folder / f"{file_stem}.step"
    stl_path = export_folder / f"{file_stem}.stl"

    cfd_step_path = export_folder / f"{file_stem}_cfd.step"

    cq.exporters.export(
        aircraft,
        str(step_path),
    )

    cq.exporters.export(
        aircraft,
        str(cfd_step_path),
        exportType="STEP",
    )

    cq.exporters.export(
        aircraft,
        str(stl_path),
    )

    exported_files = {
        "STEP": step_path,
        "CFD STEP": cfd_step_path,
        "STL": stl_path,
    }

    for export_name, export_path in exported_files.items():
        if not export_path.exists():
            raise RuntimeError(
                f"{export_name} export failed: {export_path} was not created."
            )

        if export_path.stat().st_size == 0:
            raise RuntimeError(
                f"{export_name} export failed: {export_path} is empty."
            )

    print("\nCAD EXPORT")
    print("-" * 72)
    print(f"Configuration:          {configuration_name}")
    print(f"Valid geometry:         {aircraft.isValid()}")
    print(f"Connected solid count:  {solid_count}")
    print(f"STEP file:              {step_path}")
    print(f"STL file:               {stl_path}")
    print(f"CFD-ready STEP file:    {cfd_step_path}")
    print("Export validation:      PASSED")

    show(
        aircraft,
        names=[f"{configuration_name} Aircraft"],
    )

    return aircraft
