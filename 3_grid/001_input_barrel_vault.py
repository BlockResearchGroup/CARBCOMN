from math import radians
from pathlib import Path

from compas_viewer import Viewer
from compas_viewer.config import Config

from compas import json_dump
from compas.datastructures import Mesh
from compas.geometry import Frame
from compas.geometry import Rotation
from compas.geometry import add_vectors
from compas.geometry import angle_vectors
from compas.geometry import subtract_vectors
from compas.geometry import transform_points
from compas.geometry import translate_points


def from_barrel_vault(
    span: float = 6.0,
    length: float = 6.0,
    thickness: float = 0.25,
    rise: float = 0.6,
    vou_span: int = 9,
    vou_length: int = 6,
    zero_is_centerline_or_lowestpoint: bool = False,
) -> tuple[list[Mesh], list[Frame]]:
    """
    Creates block elements from the barrel vault geometry.

    Parameters
    ----------
    span : float
        span of the vault
    length : float
        length of the vault perpendicular to the span
    thickness : float
        thickness of the vault
    rise : float
        rise of the vault from 0.0 to middle axis of the vault thickness
    vou_span : int
        number of voussoirs in the span direction
    vou_length : int
        number of voussoirs in the length direction
    zero_is_centerline_or_lowestpoint : bool
        if True, the lowest point of the vault is at the center line of the arch, otherwise the center line of the vault is lowest mesh z-coordinate.

    Returns
    -------
    tuple[list[`compas.datastructures.Mesh`], list[`compas.geometry.Frame`]]
        A tuple containing the block meshes and the frames of the blocks.
    """
    radius = rise / 2 + span**2 / (8 * rise)
    top = [0, 0, rise]
    left = [-span / 2, 0, 0]
    center = [0.0, 0.0, rise - radius]
    vector = subtract_vectors(left, center)
    springing = angle_vectors(vector, [-1.0, 0.0, 0.0])
    sector = radians(180) - 2 * springing
    angle = sector / vou_span

    a = [0, -length / 2, rise - (thickness / 2)]
    d = add_vectors(top, [0, -length / 2, (thickness / 2)])

    R = Rotation.from_axis_and_angle([0, 1.0, 0], 0.5 * sector, center)
    bottom = transform_points([a, d], R)
    brick_pts = []
    for i in range(vou_span + 1):
        R_angle = Rotation.from_axis_and_angle([0, 1.0, 0], -angle * i, center)
        points = transform_points(bottom, R_angle)
        brick_pts.append(points)

    depth = length / vou_length
    grouped_data = [pair[0] + pair[1] for pair in zip(brick_pts, brick_pts[1:])]

    meshes = []
    for i in range(vou_length):
        for l, group in enumerate(grouped_data):  # noqa: E741
            is_support = l == 0 or l == (len(grouped_data) - 1)
            if l % 2 == 0:
                point_l = [group[0], group[1], group[2], group[3]]
                point_list = [
                    [group[0][0], group[0][1] + (depth * i), group[0][2]],
                    [group[1][0], group[1][1] + (depth * i), group[1][2]],
                    [group[2][0], group[2][1] + (depth * i), group[2][2]],
                    [group[3][0], group[3][1] + (depth * i), group[3][2]],
                ]
                p_t = translate_points(point_l, [0, depth * (i + 1), 0])
                vertices = point_list + p_t
                faces = [[0, 1, 3, 2], [0, 4, 5, 1], [4, 6, 7, 5], [6, 2, 3, 7], [1, 5, 7, 3], [2, 6, 4, 0]]
                mesh = Mesh.from_vertices_and_faces(vertices, faces)
                mesh.attributes["is_support"] = is_support
                meshes.append(mesh)
            else:
                point_l = [group[0], group[1], group[2], group[3]]
                points_base = translate_points(point_l, [0, depth / 2, 0])
                points_b_t = translate_points(points_base, [0, depth * i, 0])
                points_t = translate_points(points_base, [0, depth * (i + 1), 0])
                vertices = points_b_t + points_t
                if i != vou_length - 1:
                    faces = [[0, 1, 3, 2], [0, 4, 5, 1], [4, 6, 7, 5], [6, 2, 3, 7], [1, 5, 7, 3], [2, 6, 4, 0]]
                    mesh = Mesh.from_vertices_and_faces(vertices, faces)
                    mesh.attributes["is_support"] = is_support
                    meshes.append(mesh)

    for l, group in enumerate(grouped_data):  # noqa: E741
        is_support = l == 0 or l == (len(grouped_data) - 1)
        if l % 2 != 0:
            point_l = [group[0], group[1], group[2], group[3]]
            p_t = translate_points(point_l, [0, depth / 2, 0])
            vertices = point_l + p_t
            faces = [[0, 1, 3, 2], [0, 4, 5, 1], [4, 6, 7, 5], [6, 2, 3, 7], [1, 5, 7, 3], [2, 6, 4, 0]]
            mesh = Mesh.from_vertices_and_faces(vertices, faces)
            mesh.attributes["is_support"] = is_support
            meshes.append(mesh)

            point_f = translate_points(point_l, [0, length, 0])
            p_f = translate_points(point_f, [0, -depth / 2, 0])
            vertices = p_f + point_f
            faces = [[0, 1, 3, 2], [0, 4, 5, 1], [4, 6, 7, 5], [6, 2, 3, 7], [1, 5, 7, 3], [2, 6, 4, 0]]
            mesh = Mesh.from_vertices_and_faces(vertices, faces)
            mesh.attributes["is_support"] = is_support
            meshes.append(mesh)

    # Find the lowest z-coordinate and move all the block to zero.
    if not zero_is_centerline_or_lowestpoint:
        min_z = min([min(mesh.vertex_coordinates(key)[2] for key in mesh.vertices()) for mesh in meshes])
        for mesh in meshes:
            mesh.translate([0, 0, -min_z])

    frames = []
    for i, mesh in enumerate(meshes):
        frame = Frame(mesh.face_polygon(5).frame.point, mesh.vertex_point(0) - mesh.vertex_point(2), mesh.vertex_point(4) - mesh.vertex_point(2))
        frames.append(frame)

    return meshes, frames


# Add blocks, by moving them by the height of the first column.
barrel_vault = from_barrel_vault(span=6000, length=6000, thickness=250, rise=600, vou_span=5, vou_length=5)

# =============================================================================
# Serialize the Barrel Vault into a JSON file.
# =============================================================================

model_input = {"meshes": barrel_vault[0], "frames": barrel_vault[1]}
json_dump(model_input, Path("data/barrel_vault.json"))

# =============================================================================
# Visualize
# =============================================================================

config = Config()
config.camera.target = [0, 0, 100]
config.camera.position = [10000, -10000, 10000]
config.camera.near = 10
config.camera.far = 100000
config.renderer.gridsize = (20000, 20, 20000, 20)

viewer = Viewer(config=config)

for mesh in barrel_vault[0]:
    viewer.scene.add(mesh, hide_coplanaredges=False)
viewer.show()
