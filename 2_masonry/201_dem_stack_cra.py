import pathlib

import compas
from compas_masonry.analysis import cra_penalty_solve
from compas_masonry.elements import BlockElement
from compas_masonry.models import BlockModel
from compas_masonry.viewers import BlockModelViewer

# =============================================================================
# Load model
# =============================================================================

model: BlockModel = compas.json_load(pathlib.Path(__file__).parent / "data/stack.json")

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
