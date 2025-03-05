from pathlib import Path

import compas
from compas.geometry import Brep
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
# Compute Contacts
# =============================================================================

model.compute_contacts(tolerance=1, minimum_area=1, k=6)

# =============================================================================
# Preprocess
# =============================================================================

TOL.lineardeflection = 1
TOL.angulardeflection = 1

elements = list(model.elements())

columns = [element for element in elements if isinstance(element, ColumnElement)]
beams = [element for element in elements if isinstance(element, BeamProfileElement)]

blocks = []
for element in elements:
    if isinstance(element, BlockElement):
        brep = Brep.from_mesh(element.modelgeometry)
        brep.simplify(lineardeflection=TOL.lineardeflection, angulardeflection=TOL.angulardeflection)
        blocks.append(brep)

contacts = []
for edge in model.graph.edges():
    if model.graph.edge_attribute(edge, "contacts"):
        polygons = []
        for contact in model.graph.edge_attribute(edge, "contacts"):
            polygons += contact.mesh.to_polygons()
        brep = Brep.from_polygons(polygons)
        brep.simplify(lineardeflection=TOL.lineardeflection, angulardeflection=TOL.angulardeflection)
        contacts.append(brep)

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
    show_faces=False,
    name="Blocks",
)

viewer.scene.add(
    contacts,
    facecolor=(0, 255, 0),
    name="Contacts",
)

viewer.show()
