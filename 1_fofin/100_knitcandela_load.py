import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Cylinder
from compas_viewer import Viewer

# ==============================================================================
# Define the data files
# ==============================================================================

here = pathlib.Path(__file__).parent
cablemeshpath = here / "data" / "CableMesh.json"
sessionpath = here / "data" / "session.json"

# ==============================================================================
# Load the cablemesh
# ==============================================================================

cablemesh: Mesh = compas.json_load(cablemeshpath)

for vertex in cablemesh.vertices():
    cablemesh.unset_vertex_attribute(vertex, "constraint")

# ==============================================================================
# Define and export a work session
# ==============================================================================

session = {
    "cablemesh": cablemesh,
    "params": {
        "thickness": 0.15,
        "ribs": 0.05,
        "shell": 0.05,
    },
}

compas.json_dump(session, sessionpath)

# ==============================================================================
# Viz
# ==============================================================================

viewer = Viewer()

viewer.renderer.camera.target = [0, 0, 2]
viewer.renderer.camera.position = [3, -7, 3]

viewer.scene.add(cablemesh, color=Color.red())

# for edge in cablemesh.edges():
#     viewer.scene.add(
#         Cylinder.from_line_and_radius(cablemesh.edge_line(edge), radius=0.05 * cablemesh.edge_attribute(edge, "_f")), facecolor=Color.red(), linecolor=Color.red().contrast
#     )

viewer.show()
