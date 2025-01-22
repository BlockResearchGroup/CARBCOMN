import math
import pathlib
import random

import compas
from compas.colors import Color
from compas.geometry import Box
from compas_masonry.models import BlockModel
from compas_viewer import Viewer

# =============================================================================
# Block Geometry
# =============================================================================

box = Box.from_corner_corner_height([0, 0, 0], [1, 1, 0], 1)

blocks: list[Box] = []
for i in range(10):
    block: Box = box.copy()
    block.translate(
        [
            random.choice([-0.1, +0.1]) * random.random(),
            random.choice([-0.1, +0.1]) * random.random(),
            i * box.zsize,
        ]
    )
    block.rotate(math.radians(random.choice([-5, +5])), box.frame.zaxis, box.frame.point)
    blocks.append(block)

# =============================================================================
# Model and interactions
# =============================================================================

model = BlockModel.from_boxes(blocks)

model.compute_contacts()

# =============================================================================
# Export
# =============================================================================

compas.json_dump(model, pathlib.Path(__file__).parent / "data/stack.json")

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

for element in model.elements():
    viewer.scene.add(element.modelgeometry, show_faces=False)

for contact in model.contacts():
    viewer.scene.add(contact.polygon, facecolor=Color.green())

viewer.show()
