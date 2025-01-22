"""
1.
"""

import pathlib

from compas.geometry import Box

box = Box(1)

filepath = pathlib.Path(__file__).parent / "box.json"

box.to_json(filepath)
