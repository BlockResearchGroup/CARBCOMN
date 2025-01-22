import pathlib

import compas
from compas.colors import Color
from compas_masonry.models import BlockModel
from compas_masonry.templates import BarrelVaultTemplate
from compas_viewer import Viewer
from compas_viewer.config import Config

# =============================================================================
# Template
# =============================================================================

template = BarrelVaultTemplate(span=6000, length=6000, thickness=250, rise=600, vou_span=5, vou_length=5)

# =============================================================================
# Model and interactions
# =============================================================================

model = BlockModel.from_barrelvault(template)

model.compute_contacts(k=6)

# =============================================================================
# Export
# =============================================================================

compas.json_dump(model, pathlib.Path(__file__).parent.parent / "data" / "barrel.json")

# =============================================================================
# Viz
# =============================================================================

config = Config()
config.camera.target = [0, 1000, 1250]
config.camera.position = [0, -10000, 8125]
config.camera.near = 10
config.camera.far = 100000
config.camera.pandelta = 100
config.renderer.gridsize = (20000, 20, 20000, 20)

viewer = Viewer(config=config)

for element in model.elements():
    viewer.scene.add(element.modelgeometry, show_faces=False)

for contact in model.contacts():
    viewer.scene.add(contact.polygon, facecolor=Color.green())

viewer.show()