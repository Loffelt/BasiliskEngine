import basilisk as bsk
import glm
from math import cos, sin
import pygame as pg

class App():
    def __init__(self):
        self.engine = bsk.Engine(grab_mouse=False)
        self.scene = bsk.Scene()

        self.engine.scene = self.scene

        self.scene.camera = bsk.StaticCamera(position=(0, 0, 4))

        self.sphere_mesh = bsk.Mesh('tests/sphere.obj')
        self.mud = bsk.Image('tests/mud.png')
        self.mud_normal = bsk.Image('tests/mud_normal.png')
        self.cloth_albedo = bsk.Image('tests/cloth_albedo.png')
        self.cloth_normal = bsk.Image('tests/cloth_normal.png')
        self.mtl = bsk.Material(texture=self.mud, normal=self.mud_normal)
       
        self.node = self.scene.add_node(mesh=self.sphere_mesh, material=self.mtl)

        self.cam_rot = 0

    def update(self):
        if self.engine.keys[pg.K_1]:
            self.scene.camera = bsk.StaticCamera(position=(0, 0, 4))
            self.engine.mouse.grab = False
        if self.engine.keys[pg.K_2]:
            self.scene.camera = bsk.FreeCamera(position=(0, 0, 4))
            self.engine.mouse.grab = True
        if self.engine.keys[pg.K_3]:
            self.engine.mouse.set_pos(400, 400)

        if self.engine.mouse.left_down:
            if 30 < self.engine.mouse.y < 60:
                self.cam_rot = min(max((self.engine.mouse.x - 90) / 200, 0.0), 1.0)
                self.scene.light_handler.directional_light.direction = (cos(self.cam_rot * 6.28), -.5, sin(self.cam_rot * 6.28))
            if 60 < self.engine.mouse.y < 90:
                self.mtl.roughness = min(max((self.engine.mouse.x - 90) / 200, 0.0), 1.0)
            if 90 < self.engine.mouse.y < 120:
                self.mtl.sheen = min(max((self.engine.mouse.x - 90) / 200, 0.0), 1.0)
            if 120 < self.engine.mouse.y < 150:
                self.mtl.subsurface = min(max((self.engine.mouse.x - 90) / 200, 0.0), 1.0)

    def draw(self):
        self.draw_slider(1, self.cam_rot, title="Light")
        self.draw_slider(2, self.mtl.roughness, title="Roughness")
        self.draw_slider(3, self.mtl.sheen, title="Sheen")
        self.draw_slider(4, self.mtl.subsurface, title="Subsurface")

    def draw_slider(self, y, value, title=None):
        if title: bsk.draw.text(self.engine, title, (45, y * 30 + 15), scale=0.25)
        bsk.draw.rect(self.engine, (100, 100, 100, 150), (90, y * 30 + 10, 200, 10))
        bsk.draw.rect(self.engine, (200, 200, 200, 150), (90 + value * 200, y * 30 + 5, 10, 20))

    def start(self):
        while self.engine.running:
            self.update()
            self.draw()
            self.engine.update()

app = App()
app.start()