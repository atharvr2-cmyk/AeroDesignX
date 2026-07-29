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
    """Create one tapered half-wing from lofted airfoil sections."""

    root_airfoil_points = generate_naca_4_digit_points(
        chord_mm=root_chord_mm,
        thickness_ratio=0.12,
    )

    tip_airfoil_points = generate_naca_4_digit_points(
        chord_mm=tip_chord_mm,
        thickness_ratio=0.10,
    )

    tip_y = side * semi_span_mm

    tip_z = semi_span_mm * sin(
        dihedral_deg * pi / 180.0
    )

    root_plane = cq.Plane(
        origin=(0.0, 0.0, 0.0),
        xDir=(1.0, 0.0, 0.0),
        normal=(0.0, side, 0.0),
    )

    tip_plane = cq.Plane(
        origin=(sweep_mm, tip_y, tip_z),
        xDir=(1.0, 0.0, 0.0),
        normal=(0.0, side, 0.0),
    )

    root_wire = (
        cq.Workplane(root_plane)
        .polyline(root_airfoil_points)
        .close()
        .val()
    )

    tip_wire = (
        cq.Workplane(tip_plane)
        .polyline(tip_airfoil_points)
        .close()
        .val()
    )

    half_wing = cq.Solid.makeLoft(
        [root_wire, tip_wire],
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

    fuselage_length_mm = meters_to_millimeters(
        component_sizes["fuselage_length"]
    )
    fuselage_width_mm = meters_to_millimeters(
        component_sizes["fuselage_width"]
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
        height_mm=1.15 * fuselage_width_mm,
        wing_leading_edge_x_mm=0.0,
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

    fuselage_tail_x_mm = 0.70 * fuselage_length_mm

    # Move the tail forward enough to overlap the rear fuselage.
    tail_leading_edge_x_mm = (
        fuselage_tail_x_mm
        - 0.75 * horizontal_tail_root_mm
    )

    horizontal_tail = create_complete_wing(
        span_mm=horizontal_tail_span_mm,
        root_chord_mm=horizontal_tail_root_mm,
        tip_chord_mm=horizontal_tail_tip_mm,
        sweep_mm=0.20 * horizontal_tail_root_mm,
        dihedral_deg=0.0,
    ).translate(
        (tail_leading_edge_x_mm, 0.0, 10.0)
    )

    vertical_tail = create_half_wing(
        semi_span_mm=vertical_tail_height_mm,
        root_chord_mm=vertical_tail_root_mm,
        tip_chord_mm=vertical_tail_tip_mm,
        sweep_mm=0.30 * vertical_tail_root_mm,
        dihedral_deg=0.0,
        side=1,
    ).rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        90.0,
    ).translate(
        (tail_leading_edge_x_mm, 0.0, 0.0)
    )

    conventional_aircraft = (
        main_wing
        .fuse(fuselage)
        .fuse(horizontal_tail)
        .fuse(vertical_tail)
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

    center_body = create_streamlined_fuselage(
        length_mm=0.62 * fuselage_length_mm,
        width_mm=fuselage_width_mm,
        height_mm=1.10 * fuselage_width_mm,
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

    tail_x_mm = (
        boom_start_x_mm
        + boom_length_mm
        - 0.70 * horizontal_tail_root_mm
    )

    horizontal_tail = create_complete_wing(
        span_mm=horizontal_tail_span_mm,
        root_chord_mm=horizontal_tail_root_mm,
        tip_chord_mm=horizontal_tail_tip_mm,
        sweep_mm=0.20 * horizontal_tail_root_mm,
        dihedral_deg=0.0,
    ).translate(
        (tail_x_mm, 0.0, boom_z_mm)
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
        (tail_x_mm, boom_y_mm, boom_z_mm)
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
        (tail_x_mm, -boom_y_mm, boom_z_mm)
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


def create_flying_wing_aircraft(
    wing_geometry: dict,
    component_sizes: dict,
) -> cq.Shape:
    """Create a flying-wing UAV using AeroDesignX sizing results."""

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

    flying_wing = create_complete_wing(
        span_mm=span_mm,
        root_chord_mm=root_chord_mm,
        tip_chord_mm=tip_chord_mm,
        sweep_mm=sweep_mm,
        dihedral_deg=dihedral_deg,
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

    cq.exporters.export(
        aircraft,
        str(step_path),
    )

    cq.exporters.export(
        aircraft,
        str(stl_path),
    )

    print("\nCAD EXPORT")
    print("-" * 72)
    print(f"Configuration:          {configuration_name}")
    print(f"Valid geometry:         {aircraft.isValid()}")
    print(f"Connected solid count:  {solid_count}")
    print(f"STEP file:              {step_path}")
    print(f"STL file:               {stl_path}")

    return aircraft
