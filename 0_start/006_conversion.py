from compas.colors import Color
from compas.geometry import Box
from compas_viewer import Viewer

box = Box(1)

poly = box.to_polyhedron()
mesh = box.to_mesh()
brep = box.to_brep()

viewer = Viewer()
viewer.scene.add(
    poly,
    facecolor=Color.green(),
    linecolor=Color.blue(),
    show_points=True,
    pointsize=10,
    pointcolor=Color.red(),
)
viewer.show()
