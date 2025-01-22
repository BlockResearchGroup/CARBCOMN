#! python3
# venv: carbcomn
# r: compas

"""
1. Make a box.
2. Add the box to a scene.
3. Draw the scene.
4. Change color.
5. Delete previous objects.
"""

from compas.geometry import Box
from compas.scene import Scene

box = Box(1, 1, 1)

scene = Scene()
scene.add(box)
