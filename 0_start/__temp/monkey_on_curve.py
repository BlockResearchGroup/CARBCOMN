import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Frame
from compas.geometry import NurbsCurve
from compas.geometry import Transformation
from compas.itertools import linspace
from compas_viewer import Viewer
from compas_viewer.config import Config

session = compas.json_load("/Users/vanmelet/session.json")

curve: NurbsCurve = session["curve"]
monkey: Mesh = session["monkey"]

frames: list[Frame] = []
for t in linspace(curve.domain[0], curve.domain[1], 100):
    frames.append(curve.frame_at(t))

transformations = []
for frame in frames:
    transformations.append(Transformation.from_frame_to_frame(frame.worldXY(), frame))

config = Config()
config.camera.target = [0, 3, 1.5]
config.camera.position = [0, -6, 2.5]

viewer = Viewer(config=config)

viewer.scene.add(curve)

for frame in frames[::3]:
    viewer.scene.add(frame, framesize=[0.15, 2, 0.15, 2])

obj = viewer.scene.add(monkey, facecolor=Color.from_hex("#0092d2"))


@viewer.on(interval=100, frames=len(transformations))
def slide(f):
    obj.transformation = transformations[f]
    obj.update_matrix()


viewer.show()
