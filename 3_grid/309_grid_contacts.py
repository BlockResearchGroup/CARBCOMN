from pathlib import Path

import compas
from compas.geometry import Brep
from compas.tolerance import TOL
from compas_grid import GridModel
from compas_grid.elements import BeamTProfileElement
from compas_grid.elements import BlockElement
from compas_grid.elements import ColumnSquareElement
from compas_viewer import Viewer
from compas_viewer.config import Config

# =============================================================================
# JSON file with the geometry of the model.
# =============================================================================

rhino_geometry = compas.json_load(Path(__file__).parent.parent / "data" / "frame.json")
lines = rhino_geometry["lines"]
meshes = rhino_geometry["meshes"]

# =============================================================================
# Model
# =============================================================================

model = GridModel.from_lines_and_surfaces(columns_and_beams=lines, floor_surfaces=meshes)

edges_columns = list(model.cell_network.edges_where({"is_column": True}))  # Order as in the model
edges_beams = list(model.cell_network.edges_where({"is_beam": True}))  # Order as in the model
faces_floors = list(model.cell_network.faces_where({"is_floor": True}))  # Order as in the model

# =============================================================================
# Add Column on a CellNetwork Edge
# =============================================================================

for edge in edges_columns:
    column = ColumnSquareElement(300, 300)
    model.add_column(column, edge)

# =============================================================================
# Add Beams on a CellNetwork Edge
# =============================================================================

for edge_index in [0, 3]:
    beam = BeamTProfileElement(width=300, height=700, step_width_left=75, step_height_left=150)
    model.add_beam(beam, edges_beams[edge_index], 150)

# =============================================================================
# Add Plates on a CellNetwork Face
# =============================================================================

barrel_vault = compas.json_load(Path(__file__).parent.parent / "data" / "barrel.json")
for face in faces_floors:
    for barrel_vault_element in list(barrel_vault.elements()):
        block = BlockElement(shape=barrel_vault_element.shape, is_support=barrel_vault_element.is_support, transformation=barrel_vault_element.transformation)
        model.add_floor(block, face)


# =============================================================================
# Process elements
# =============================================================================
elements = list(model.elements())
columns = [element for element in elements if isinstance(element, ColumnSquareElement)]
beams = [element for element in elements if isinstance(element, BeamTProfileElement)]
blocks = [element for element in elements if isinstance(element, BlockElement)]

# =============================================================================
# Add Interactions
# =============================================================================

elements = list(model.elements())
beams = [element for element in elements if isinstance(element, BeamTProfileElement)]
for beam in beams:
    for block in blocks:
        model.add_interaction(beam, block)
        model.add_modifier(beam, block)  # beam -> cuts -> block


# =============================================================================
# Compute Contacts
# =============================================================================

model.compute_contacts(tolerance=1, minimum_area=1, k=8)

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

viewer.scene.add([e.modelgeometry for e in columns], show_faces=True, opacity=0.7, name="Columns", hide_coplanaredges=True)

viewer.scene.add([e.modelgeometry for e in beams], show_faces=False, name="Beams", hide_coplanaredges=True)

viewer.scene.add([e.modelgeometry for e in blocks], show_faces=False, name="Blocks", hide_coplanaredges=True)

viewer.scene.add(
    contacts,
    facecolor=(0, 255, 0),
    name="Contacts",
)


viewer.show()
