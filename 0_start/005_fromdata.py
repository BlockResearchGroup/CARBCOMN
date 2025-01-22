#! python3
# venv: carbcomn
# r: compas

import pathlib

from compas.colors import Color
from compas.geometry import Box
from compas.scene import Scene

filepath = pathlib.Path(__file__).parent / "box.json"

box = Box.from_json(filepath)

scene = Scene()
scene.clear_context()
scene.add(box, color=Color.green())
scene.draw()
