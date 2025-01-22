from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import boolean_difference_mesh_mesh
from compas_viewer import Viewer

box = Box(2)
sphere: Sphere = Sphere(radius=1.0, point=[1, 1, 1])

# result = box.to_brep() - sphere.to_brep()

result = Mesh.from_vertices_and_faces(
    *boolean_difference_mesh_mesh(
        box.to_vertices_and_faces(triangulated=True),
        sphere.to_vertices_and_faces(triangulated=True, u=64),
    )
)

viewer = Viewer()
viewer.scene.add(
    result,
    facecolor=Color.green(),
)
viewer.show()
