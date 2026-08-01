from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys

from flask import Flask, render_template, request


WEB_DIR = Path(__file__).resolve().parent
PROJECT_DIR = WEB_DIR.parent

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from config.parameters import (
    AIRFOIL,
    AIR_DENSITY,
    CL_MAX,
    DIHEDRAL,
    GRAVITY,
    MASS,
    PAYLOAD_MASS,
    SWEEP,
)
from design.configurations import recommend_configuration
from missions.profiles import get_mission
from missions.requirements import calculate_mission_requirements
from optimization.optimizer import optimize_aircraft



app = Flask(
    __name__,
    template_folder=str(WEB_DIR / "templates"),
    static_folder=str(WEB_DIR / "static"),
)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/design", methods=["POST"])
def design():
    form_data = {
        "mission": request.form["mission"],
        "payload_mass": float(request.form["payload_mass"]),
        "cruise_speed": float(request.form["cruise_speed"]),
        "max_wingspan": float(request.form["max_wingspan"]),
        "battery_capacity": float(
            request.form["battery_capacity"]
        ),
        "configuration": request.form["configuration"],
    }

    mission_configuration_names = {
        "cargo": "Cargo",
        "survey": "Survey",
        "trainer": "Trainer",
        "racing": "Racing",
        "vtol_support": "VTOL Support",
    }

    mission_profile_names = {
        "cargo": "cargo",
        "survey": "surveillance",
        "trainer": "trainer",
        "racing": "racing",
        "vtol_support": "trainer",
    }

    configuration_names = {
        "conventional": "Conventional",
        "twin_boom": "Twin Boom",
        "flying_wing": "Flying Wing",
    }

    mission_name = mission_configuration_names[
        form_data["mission"]
    ]

    mission_profile_name = mission_profile_names[
        form_data["mission"]
    ]

    selected_mission = get_mission(
        mission_profile_name
    )

    empty_aircraft_mass = MASS - PAYLOAD_MASS

    mission_requirements = calculate_mission_requirements(
        selected_mission,
        base_aircraft_mass=empty_aircraft_mass,
        gravity=GRAVITY,
    )

    total_mass = (
        empty_aircraft_mass
        + form_data["payload_mass"]
    )

    mission_requirements["payload_mass"] = (
        form_data["payload_mass"]
    )

    mission_requirements["total_mass"] = total_mass

    mission_requirements["required_lift"] = (
        total_mass * GRAVITY
    )

    mission_requirements["cruise_speed"] = (
        form_data["cruise_speed"]
    )

    required_endurance_hours = mission_requirements[
        "required_endurance_hours"
    ]

    distance_at_cruise_km = (
        form_data["cruise_speed"]
        * required_endurance_hours
        * 3.6
    )

    mission_requirements["cruise_distance_km"] = (
        distance_at_cruise_km
    )

    mission_requirements["required_range_km"] = max(
        mission_requirements["stated_range_km"],
        distance_at_cruise_km,
    )

    configuration_result = recommend_configuration(
        mission_name=mission_name,
        payload_mass=form_data["payload_mass"],
        cruise_speed=form_data["cruise_speed"],
        max_wingspan=form_data["max_wingspan"],
        battery_capacity=form_data["battery_capacity"],
    )

    if form_data["configuration"] == "automatic":
        selected_configuration = configuration_result["name"]
    else:
        selected_configuration = configuration_names[
            form_data["configuration"]
        ]

    optimizer_output = StringIO()

    with redirect_stdout(optimizer_output):
        best_design = optimize_aircraft(
            number_of_designs=1000,
            span_bounds=(
                max(
                    0.1,
                    min(
                        0.90,
                        form_data["max_wingspan"] * 0.65,
                    ),
                ),
                form_data["max_wingspan"],
            ),
            root_chord_bounds=(0.24, 0.36),
            tip_chord_bounds=(0.16, 0.28),
            cruise_speed_bounds=(
                max(
                    1.0,
                    form_data["cruise_speed"] * 0.85,
                ),
                form_data["cruise_speed"] * 1.05,
            ),
            airfoil=AIRFOIL,
            sweep=SWEEP,
            dihedral=DIHEDRAL,
            mass=total_mass,
            gravity=GRAVITY,
            air_density=AIR_DENSITY,
            cl_max=CL_MAX,
            top_n=10,
            random_seed=42,
            mission_requirements=mission_requirements,
            mission_name=mission_profile_name,
        )

    results = {
        "mission": mission_name,
        "configuration": selected_configuration,
        "mission_score": round(
            best_design["mission_score"],
            2,
        ),
        "aerodynamic_score": round(
            best_design["aerodynamic_score"],
            2,
        ),
        "wingspan": best_design["span"],
        "cruise_speed": round(
            best_design["cruise_speed"],
            2,
        ),
        "payload_mass": form_data["payload_mass"],
        "battery_capacity": form_data["battery_capacity"],
        "aspect_ratio": round(
            best_design["aspect_ratio"],
            2,
        ),
        "lift_to_drag": round(
            best_design["lift_to_drag"],
            2,
        ),
        "stall_speed": round(
            best_design["stall_speed"],
            2,
        ),
        "validation": (
            "PASSED"
            if best_design.get("feasible", False)
            else "REVIEW REQUIRED"
        ),
    }

    return render_template(
        "results.html",
        results=results,
    )


if __name__ == "__main__":
    app.run(debug=True)