from compas.geometry import Box
from compas.scene import Scene

box = Box(1, 1, 1)

print(box)
print(box.to_jsonstring(pretty=True))

# scene = Scene()
# scene.add(box)
# print(scene)
# # scene.draw()
