import pathlib
import time

import compas
import compas_fea2
import numpy
from compas.colors import Color
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Brep
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Sphere
from compas.tolerance import Tolerance
from compas.utilities import print_profile
from compas_fea2.model import DeformablePart
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import Model
from compas_fea2.model import PinnedBC
from compas_fea2.model import SolidSection
from compas_fea2.problem import DisplacementFieldOutput
from compas_fea2.problem import LoadCombination
from compas_fea2.problem import Problem
from compas_fea2.problem import ReactionFieldOutput
from compas_fea2.units import units
from compas_viewer import Viewer
from compas_viewer.config import Config
from compas_viewer.scene import BufferGeometry
from compas_viewer.scene import Collection

compas_fea2.set_backend("compas_fea2_opensees")

units = units(system="SI_mm")

tolerance = Tolerance()
tolerance.absolute = 1e-9
tolerance.relative = 1e-3
tolerance.precision = 3
tolerance.lineardeflection = 1


@print_profile
def stressvectors_from_result(stress, step):
    tension = []
    compression = []

    for r in stress.results(step):
        point = r.location.reference_point
        for val, vec in r.principal_stresses:
            v1 = vec * +500
            v2 = vec * -500
            l1 = Line.from_point_and_vector(point, v1)
            l2 = Line.from_point_and_vector(point, v2)
            if val > 0:
                tension.append(l1)
                tension.append(l2)
            else:
                compression.append(l1)
                compression.append(l2)

    return numpy.asarray(compression), numpy.asarray(tension)


@print_profile
def stressmesh_from_result(part, stress, step, cmap):
    stressmesh: Mesh = part.discretized_boundary_mesh
    gkey_vertex = stressmesh.gkey_vertex()

    vertex_color = {}
    node_stress = {}

    for result in stress.results(step):
        n = len(result.location.nodes)
        for node in result.location.nodes:
            if node not in node_stress:
                node_stress[node] = 2.0
            node_stress[node] += result.von_mises_stress / n

    values = list(node_stress.values())
    min_value = min(values)
    max_value = max(values)

    for node, value in node_stress.items():
        color = cmap(value, minval=min_value, maxval=max_value)
        if node.gkey in gkey_vertex:
            vertex = gkey_vertex[node.gkey]
            vertex_color[vertex] = color
        else:
            print(f"not found: {node.gkey}")

    return stressmesh, vertex_color


# ==============================================================================
# Define the data files
# ==============================================================================

here = pathlib.Path(__file__).parent
sessionpath = here / "data" / "session.json"
breppath = str(here / "data" / "waffle.stp")

# ==============================================================================
# Import the session
# ==============================================================================

session = compas.json_load(sessionpath)

# =============================================================================
# Model
# =============================================================================

model = Model()

material = ElasticIsotropic(E=30 * units("GPa"), v=0.17, density=2350 * units("kg/m**3"))
section = SolidSection(material=material)

part = DeformablePart.from_step_file(breppath, section=section, meshsize_max=600)
model.add_part(part)

nodes = model.find_nodes_on_plane(plane=Plane.worldXY(), tolerance=1)
model.add_pin_bc(nodes=nodes)

model.summary()

# =============================================================================
# Problem
# =============================================================================

problem = Problem(name="SLS")

model.add_problem(problem=problem)

step = problem.add_static_step(name="TEST")
step.combination = LoadCombination.SLS()

step.add_node_pattern(part.nodes, z=-1000 * units.N)

step.add_outputs([DisplacementFieldOutput(), ReactionFieldOutput()])

# # =============================================================================
# # Analysis
# # =============================================================================

tmp = str(here / "__temp/tmp")

model.analyse_and_extract(problems=[problem], path=tmp, VERBOSE=True)

# problem.show_stress(step, show_bcs=0.05, show_vectors=1e2, plane="bottom")
# problem.show_deformed(scale_results=1000, show_original=0.2, show_bcs=0.3, show_loads=10)
problem.show_displacements(step, show_bcs=0.3, show_loads=10, show_contour=False, show_vectors=100)

disp_sls = step.displacement_field
reactions_sls = step.reaction_field

# # ==============================================================================
# # Export
# # ==============================================================================

# # compas.json_dump(session, sessionpath)

# # =============================================================================
# # Pre-process boundary conditions
# # =============================================================================

supports = []
for bc, nodes in model.bcs.items():
    for node in nodes:
        if isinstance(bc, PinnedBC):
            supports.append(Sphere(radius=30, point=node.xyz))

# # =============================================================================
# # Pre-process reactions
# # =============================================================================

# # for displacement in disp_sls.results(step):
# #     point = displacement.location.xyz
# #     vector = displacement.vector.scaled(1000)
# #     displacement.location.xyz = sum_vectors([point, vector])

# # deformed = Mesh()
# # for element in part.elements:
# #     vertices = [node.point for node in element.nodes]
# #     faces = [(0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3)]
# #     deformed.join(Mesh.from_vertices_and_faces(vertices, faces), weld=False)

reactions = []
for r in reactions_sls.results(step):
    point = r.location.xyz
    vector = r.vector
    reactions.append(Line.from_point_and_vector(point, vector * -0.3))

# # =============================================================================
# # Pre-process stress fields
# # =============================================================================

# compression, tension = stressvectors_from_result(stress_sls, step)

# cmap = ColorMap.from_palette("davos")
# stressmesh, vertex_color = stressmesh_from_result(part, stress_sls, step, cmap)

# # ==============================================================================
# # Viz prep
# # ==============================================================================

# # geometry = Brep.from_step(breppath)

# # ==============================================================================
# # Viz
# # ==============================================================================

# config = Config()
# config.renderer.show_gridz = False
# config.camera.target = [0, 0, 2000]
# config.camera.position = [3000, -7000, 3000]
# config.camera.near = 1e0
# config.camera.far = 1e5
# config.camera.pandelta = 100
# config.renderer.gridsize = (20000, 20, 20000, 20)

# viewer = Viewer(config=config)

# # structure = [
# #     (geometry, {"name": "Geometry", "show_faces": False, "opacity": 0.5, "linecolor": Color(0.3, 0.3, 0.3)}),
# #     (Collection(supports), {"name": "Supports", "facecolor": Color.red().lightened(50)}),
# # ]
# # viewer.scene.add(structure, name="Structure")

# # results = [
# #     # (deformed, {"name": "Deformed Geometry", "show_faces": True, "facecolor": Color(0.8, 0.8, 0.8), "linecolor": Color(0.75, 0.75, 0.75)}),
# #     (Collection(reactions), {"name": "Reactions", "linecolor": Color.green().darkened(50), "linewidth": 3}),
# #     # (stressmesh, {"name": "Von Mises Stress", "vertexcolor": vertex_color, "use_vertexcolors": True}),
# # ]
# # viewer.scene.add(results, name="Results")
# # viewer.scene.add(stressmesh, name="Von Mises Stresses", vertexcolor=vertex_color, use_vertexcolors=True)

# viewer.scene.add(BufferGeometry(lines=compression, linecolor=numpy.array([[0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0] for i in range(len(compression))])))
# viewer.scene.add(BufferGeometry(lines=tension, linecolor=numpy.array([[1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0] for i in range(len(tension))])))

# viewer.show()
