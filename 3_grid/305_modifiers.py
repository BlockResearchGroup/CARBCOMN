from pathlib import Path

import compas
from compas.datastructures import Mesh
from compas.geometry import Brep
from compas.geometry import Frame
from compas.geometry import Polygon
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import distance_point_point
from compas.tolerance import TOL
from compas_grid.elements import BeamProfileElement
from compas_grid.elements import BlockElement
from compas_grid.elements import ColumnElement
from compas_model.models import Model
from compas_viewer import Viewer
from compas_viewer.config import Config

# =============================================================================
# Load Model
# =============================================================================

model: Model = compas.json_load(Path(__file__).parent.parent / "data" / "model_with_interactions.json")

# =============================================================================
# Add Interactions
# =============================================================================

elements = list(model.elements())
blocks = [element for element in elements if isinstance(element, BlockElement)]
beams = [element for element in elements if isinstance(element, BeamProfileElement)]
for beam in beams:
    for block in blocks:
        model.add_interaction(beam, block)
        model.add_modifier(beam, block)  # beam -> cuts -> block

# =============================================================================
# Preprocess
# =============================================================================
TOL.lineardeflection = 1
TOL.angulardeflection = 1

columns = [element for element in elements if isinstance(element, ColumnElement)]

blocks = []
for element in elements:
    if isinstance(element, BlockElement):
        mesh = element.modelgeometry
        # blocks.append(mesh)

        polygons = []
        for face in mesh.faces():
            points = [
                p
                for i, p in enumerate(mesh.face_polygon(face).points)
                if distance_point_point(p, mesh.face_polygon(face).points[(i + 1) % len(mesh.face_polygon(face).points)]) > 1
            ]
            if len(points) > 2:
                polygons.append(Polygon(points))

        mesh = Mesh.from_polygons(polygons)

        brep = Brep.from_mesh(mesh)
        brep.simplify(lineardeflection=TOL.lineardeflection, angulardeflection=TOL.angulardeflection)
        blocks.append(brep)

# =============================================================================
# Visualize
# =============================================================================
config = Config()
config.camera.target = [0, 1000, 1250]
config.camera.position = [0, -10000, 8125]
config.camera.near = 10
config.camera.far = 100000
config.camera.pandelta = 100
config.renderer.gridsize = (20000, 20, 20000, 20)

viewer = Viewer(config=config)

viewer.scene.add(
    [Brep.from_mesh(e.modelgeometry) for e in columns],
    show_faces=True,
    opacity=0.7,
    name="Columns",
)

viewer.scene.add(
    [Brep.from_mesh(e.modelgeometry) for e in beams],
    show_faces=False,
    name="Beams",
)

viewer.scene.add(
    blocks,
    show_faces=True,
    name="Blocks",
)

viewer.show()
