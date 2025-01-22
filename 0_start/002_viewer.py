from compas.geometry import Box
from compas_viewer import Viewer

box = Box(1, 1, 1)

viewer = Viewer()
viewer.scene.add(box)
viewer.show()
