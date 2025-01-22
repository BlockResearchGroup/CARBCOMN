import math
import random

from compas.colors import Color
from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Rotation
from compas.geometry import Transformation
from compas.geometry import Translation
from compas_masonry.elements import BlockElement
from compas_masonry.models import BlockModel
from compas_viewer import Viewer

# =============================================================================
# Block Geometry
# =============================================================================

box = Box(1)

# =============================================================================
# Block Frames
# =============================================================================

frames: list[Frame] = []

for i in range(10):
    T = Translation.from_vector(
        [
            random.choice([-0.1, +0.1]) * random.random(),
            random.choice([-0.1, +0.1]) * random.random(),
            i * box.zsize,
        ]
    )
    R = Rotation.from_axis_and_angle(axis=[0, 0, 1], angle=math.radians(random.choice([-5, +5])))
    X = T * R

    frames.append(Frame.from_transformation(X))

# =============================================================================
# Model and interactions
# =============================================================================

model = BlockModel()
for frame in frames:
    block = BlockElement.from_box(box)
    block.frame = frame
    model.add_element(block)

model.compute_contacts()

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

for element in model.elements():
    viewer.scene.add(element.modelgeometry, show_faces=False)
    viewer.scene.add(element.frame, show_lines=True, linewidth=3)

for contact in model.contacts():
    viewer.scene.add(contact.polygon, facecolor=Color.green())

viewer.show()
