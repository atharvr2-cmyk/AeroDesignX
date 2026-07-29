"""Verify that CadQuery and OCP CAD Viewer are working."""

import cadquery as cq
from ocp_vscode import show


test_solid = (
    cq.Workplane("XY")
    .box(40, 25, 8)
    .edges()
    .fillet(2)
)

show(test_solid)