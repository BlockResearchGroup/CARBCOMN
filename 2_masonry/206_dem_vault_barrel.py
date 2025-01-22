import pathlib

import compas
from compas.colors import Color
from compas_masonry.models import BlockModel
from compas_masonry.templates import BarrelVaultTemplate
from compas_viewer import Viewer

# =============================================================================
# Template
# =============================================================================

template = BarrelVaultTemplate()

# =============================================================================
# Model and interactions
# =============================================================================

model = BlockModel.from_barrelvault(template)

model.compute_contacts(k=6)

# =============================================================================
# Export
# =============================================================================

compas.json_dump(model, pathlib.Path(__file__).parent / "data/barrel.json")

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

for element in model.elements():
    viewer.scene.add(element.modelgeometry, show_faces=False)

for contact in model.contacts():
    viewer.scene.add(contact.polygon, facecolor=Color.green())

viewer.show()
