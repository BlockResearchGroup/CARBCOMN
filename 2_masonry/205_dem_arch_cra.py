from compas_masonry.analysis import cra_penalty_solve
from compas_masonry.elements import BlockElement
from compas_masonry.models import BlockModel
from compas_masonry.templates import ArchTemplate
from compas_masonry.viewers import BlockModelViewer

# =============================================================================
# Template
# =============================================================================

template = ArchTemplate(rise=4, span=10, thickness=0.25, depth=0.5, n=50)

# =============================================================================
# Model and interactions
# =============================================================================

model = BlockModel.from_template(template)

model.compute_contacts(k=2)

# =============================================================================
# Supports
# =============================================================================

element: BlockElement

for element in model.elements():
    if model.graph.degree(element.graphnode) == 1:
        element.is_support = True

# =============================================================================
# Equilibrium
# =============================================================================

cra_penalty_solve(model)

# =============================================================================
# Viz
# =============================================================================

viewer = BlockModelViewer(model)
viewer.show()
