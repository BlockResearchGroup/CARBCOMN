from pathlib import Path

import compas
from compas.geometry import Brep
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import Vector
from compas.tolerance import TOL
from compas_grid.elements import BeamTProfileElement
from compas_grid.elements import BlockElement
from compas_grid.elements import CableElement
from compas_grid.elements import ColumnSquareElement
from compas_model.models import Model
from compas_viewer import Viewer
from compas_viewer.config import Config

# =============================================================================
# Load Model
# =============================================================================

model: Model = compas.json_load(Path(__file__).parent / "data/model.json")

# =============================================================================
# Make vault
# =============================================================================

# =============================================================================
# Add vault blocks
# =============================================================================

# =============================================================================
# Add Interactions
# =============================================================================

# for beam in beams:
#     for block in blocks:
#         model.add_interaction(beam, block)
#         model.add_modifier(beam, block)  # beam -> cuts -> block

# =============================================================================
# Export
# =============================================================================

compas.json_dump(model, Path(__file__).parent / "data/model.json")

# =============================================================================
# Preprocess
# =============================================================================

TOL.lineardeflection = 1
TOL.angulardeflection = 1

elements = list(model.elements())

columns = [element for element in elements if isinstance(element, ColumnSquareElement)]
beams = [element for element in elements if isinstance(element, BeamTProfileElement)]

blocks = []
for element in elements:
    if isinstance(element, BlockElement):
        brep = Brep.from_mesh(element.modelgeometry)
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
    show_faces=False,
    name="Blocks",
)

viewer.show()
