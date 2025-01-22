import math
import random

from compas.geometry import Box
from compas_masonry.analysis import cra_penalty_solve
from compas_masonry.elements import BlockElement
from compas_masonry.models import BlockModel
from compas_masonry.viewers import BlockModelViewer

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
# Supports
# =============================================================================

bottom: BlockElement = sorted(model.elements(), key=lambda e: e.point.z)[0]
bottom.is_support = True

# =============================================================================
# Equilibrium
# =============================================================================

cra_penalty_solve(model)

# =============================================================================
# Viz
# =============================================================================

viewer = BlockModelViewer(model)
viewer.show()
