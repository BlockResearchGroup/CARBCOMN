import math
import random

from compas.colors import Color
from compas.geometry import Box
from compas.geometry import Rotation
from compas.geometry import Transformation
from compas.geometry import Translation
from compas_masonry.elements import BlockElement
from compas_masonry.models import BlockModel
from compas_viewer import Viewer

# =============================================================================
# Block Geometry
# =============================================================================

box = Box.from_corner_corner_height([0, 0, 0], [1, 1, 0], 1)

transformations: list[Transformation] = []
for i in range(10):
    T = Translation.from_vector(
        [
            random.choice([-0.1, +0.1]) * random.random(),
            random.choice([-0.1, +0.1]) * random.random(),
            i * box.zsize,
        ]
    )
    R = Rotation.from_axis_and_angle(box.frame.zaxis, angle=math.radians(random.choice([-5, +5])))
    X = T * R
    transformations.append(X)

# =============================================================================
# Model and interactions
# =============================================================================

model = BlockModel()
for X in transformations:
    block = BlockElement.from_box(box)
    block.transformation = X
    model.add_element(block)

# for element in model.elements():
#     element.box.ysize *= 2

model.compute_contacts()

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

for element in model.elements():
    viewer.scene.add(element.modelgeometry, show_faces=False)

for contact in model.contacts():
    viewer.scene.add(contact.polygon, facecolor=Color.green())

viewer.show()
