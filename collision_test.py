import basilisk as bsk
import pygame as pg
from math import cos, sin, pi
import glm
import time
import random

engine = bsk.Engine()
scene = bsk.Scene()
engine.scene = scene

cube_mesh = bsk.cube
sphere_mesh = bsk.Mesh('tests/sphere.obj')

mud = bsk.Image("tests/mud.png")
mud_normal = bsk.Image("tests/mud_normal.png")
mud_mtl = bsk.Material(texture=mud, normal=mud_normal)
materials = [bsk.Material(color=(255 * (i & 4), 255 * (i & 2), 255 * (i & 1))) for i in range(1, 8)]
red = bsk.Material(color=(255, 0, 0))
blue = bsk.Material(color=(0, 0, 255))

aabb_edges = []
is_pressed = False
radius = 50

for _ in range(50):
    scene.add_node(
        position=[random.uniform(-radius, radius), random.uniform(-3, -radius), random.uniform(-radius, radius)], 
        scale=[random.uniform(0.5, 2) for _ in range(3)],
        rotation=[random.uniform(-radius, radius), random.uniform(-3, -radius), random.uniform(-radius, radius)], 
        mesh=cube_mesh, 
        material=blue,
        collisions=True
    )

node = scene.add_node(
    position=[random.uniform(-radius, radius), random.uniform(-3, -radius), random.uniform(-radius, radius)], 
    scale=[random.uniform(0.5, 2) for _ in range(3)],
    rotation=[random.uniform(-radius, radius), random.uniform(-3, -radius), random.uniform(-radius, radius)], 
    mesh=cube_mesh, 
    material=blue,
    collisions=True
)

while engine.running:
    keys = pg.key.get_pressed()
    if keys[pg.K_u]: node.position += (0.01, 0, 0)
    if keys[pg.K_j]: node.position -= (0.01, 0, 0)
    if keys[pg.K_h]: node.position -= (0, 0, 0.01)
    if keys[pg.K_k]: node.position += (0, 0, 0.01)
    if keys[pg.K_o]: node.position += (0, 0.01, 0)
    if keys[pg.K_p]: node.position -= (0, 0.01, 0)
    
    possible = scene.collider_handler.resolve_broad_collisions()
    # print(possible)
    
    engine.update()