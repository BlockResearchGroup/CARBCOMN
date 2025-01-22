from compas_masonry.analysis import cra_penalty_solve

# from compas_masonry.analysis import rbe_solve
from compas_masonry.models import BlockModel
from compas_masonry.templates import BarrelVaultTemplate
from compas_masonry.viewers import BlockModelViewer

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
# Equilibrium
# =============================================================================

# rbe_solve(model)
cra_penalty_solve(model)

# =============================================================================
# Viz
# =============================================================================

viewer = BlockModelViewer(model)
viewer.show()
