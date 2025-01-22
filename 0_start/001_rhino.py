#! python3
# venv: carbcomn
# r: compas

from compas.colors import Color
from compas.geometry import Box
from compas.scene import Scene

box = Box(1, 1, 1)

scene = Scene()
scene.clear_context()
scene.add(box, color=Color.red())
scene.draw()
