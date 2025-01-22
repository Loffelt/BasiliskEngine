import basilisk as bsk
import numpy as np

engine = bsk.Engine()
scene = bsk.Scene()
engine.scene = scene

red = bsk.Material(color=(255, 0, 0))
blue = bsk.Material(color=(0, 0, 255))

quad = np.array([[0, 0, 0], [5, 0, 5], [5, 0, 0], 
                 [0, 0, 5], [5, 0, 5], [0, 0, 0]])

mesh = bsk.Mesh(quad)

scene.add_node(mesh=mesh, material=[red, red, red, blue, blue, blue])
scene.camera.position = (2, 3, 2)

while engine.running:
    engine.update()