import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Brep
from compas.geometry import Point
from compas.geometry import offset_polygon
from compas.itertools import pairwise
from compas.tolerance import Tolerance
from compas_viewer import Viewer
from compas_viewer.config import Config

# ==============================================================================
# Define the data files
# ==============================================================================

here = pathlib.Path(__file__).parent
sessionpath = here / "data" / "session.json"

# ==============================================================================
# Import the session
# ==============================================================================

session = compas.json_load(sessionpath)

# ==============================================================================
# Load the cablemesh from the work session
# ==============================================================================

cablemesh: Mesh = session["cablemesh"]
shell: Mesh = session["shell"]

params = session["params"]

cablemesh.scale(1e3)
shell.scale(1e3)

# ==============================================================================
# Make an intrados
# ==============================================================================

idos: Mesh = cablemesh.copy()

for vertex in idos.vertices():
    point = cablemesh.vertex_point(vertex)
    normal = cablemesh.vertex_normal(vertex)
    idos.vertex_attributes(vertex, "xyz", point + normal * (-params["shell"] * 1e3))

# =============================================================================
# Blocks
# =============================================================================

boxes: list[Brep] = []

vertex_point = {vertex: idos.vertex_point(vertex) for vertex in idos.vertices()}
vertex_normal = {vertex: idos.vertex_normal(vertex) for vertex in idos.vertices()}

for face in idos.faces():
    # vertices of the face
    vertices = idos.face_vertices(face)

    # coordinates and normals of the face vertices
    points = [vertex_point[vertex] for vertex in vertices]
    normals = [vertex_normal[vertex] for vertex in vertices]

    # bottom face of the box as an inward offset of the face polygon
    bottom = [Point(*point) for point in offset_polygon(points, distance=0.5 * params["ribs"] * 1e3)]

    # additional offset to create tapering
    inset = [Point(*point) for point in offset_polygon(points, distance=0.5 * params["ribs"] * 1e3)]

    # top face of the box
    top = [point + normal * params["thickness"] * 1e3 for point, normal in zip(inset, normals)]

    # box sides
    bottomloop = bottom + bottom[:1]
    toploop = top + top[:1]
    sides = []
    for (a, b), (aa, bb) in zip(pairwise(bottomloop[::-1]), pairwise(toploop[::-1])):
        sides.append([a, aa, bb, b])

    # box mesh from polygons
    polygons = [bottom[::-1], top] + sides
    box = Mesh.from_polygons(polygons)
    brep = Brep.from_mesh(box)
    boxes.append(brep)

# ==============================================================================
# Waffle
# ==============================================================================

A: Brep = Brep.from_mesh(shell)

waffle = A - boxes
waffle.fix()
waffle.sew()
waffle.make_solid()

filepath = here / "data" / "waffle.stp"
waffle.to_step(filepath)

# ==============================================================================
# Add the intrados to the session
# ==============================================================================

# ==============================================================================
# Export
# ==============================================================================

# compas.json_dump(session, sessionpath)

# ==============================================================================
# Viz
# ==============================================================================

tolerance = Tolerance()
tolerance.lineardeflection = 1

config = Config()
config.renderer.gridsize = (20000, 20, 20000, 20)
config.camera.pandelta = 100
config.camera.near = 1e0
config.camera.far = 1e5
config.camera.target = [0, 0, 2000]
config.camera.position = [3000, -7000, 3000]

viewer = Viewer(config=config)

viewer.scene.add(session["shell"])
viewer.scene.add(idos, facecolor=Color.blue().lightened(50), linecolor=Color.blue())
viewer.scene.add(waffle)

viewer.show()
