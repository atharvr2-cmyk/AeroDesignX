"""
Aircraft Design Concepts

Stores predefined aircraft configurations that can be
generated automatically.
"""

from dataclasses import dataclass


@dataclass
class AircraftConcept:
    """
    High-level aircraft design concept.
    """

    name: str
    span: float
    aspect_ratio: float
    cruise_speed: float
    description: str


TRAINER = AircraftConcept(
    name="Trainer",
    span=1.20,
    aspect_ratio=7.0,
    cruise_speed=15.0,
    description="Balanced aircraft for general-purpose flight."
)

GLIDER = AircraftConcept(
    name="Glider",
    span=2.00,
    aspect_ratio=14.0,
    cruise_speed=12.0,
    description="High-efficiency aircraft with excellent endurance."
)

RACER = AircraftConcept(
    name="Racer",
    span=0.80,
    aspect_ratio=4.0,
    cruise_speed=30.0,
    description="Fast aircraft optimized for speed."
)

HEAVY_LIFT = AircraftConcept(
    name="Heavy Lift",
    span=1.50,
    aspect_ratio=6.0,
    cruise_speed=10.0,
    description="Designed to carry heavier payloads."
)

FLYING_WING = AircraftConcept(
    name="Flying Wing",
    span=1.60,
    aspect_ratio=10.0,
    cruise_speed=20.0,
    description="Efficient tailless aircraft with low drag."
)

ALL_CONCEPTS = [
    TRAINER,
    GLIDER,
    RACER,
    HEAVY_LIFT,
    FLYING_WING
]