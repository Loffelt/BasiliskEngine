import basilisk as bsk
import pygame as pg

engine = bsk.Engine(grab_mouse=False)
scene = bsk.Scene()
engine.scene = scene

brick = bsk.Image('tests/brick.png')

# Create an image from pygame surface
surf = pg.Surface((100, 100))
surf.fill((0, 255, 255))
pg.draw.rect(surf, (255, 0, 0), (10, 10, 60, 60))
pg_img = bsk.Image(surf)

while engine.running:

    bsk.draw.rect(engine, (0, 0, 255), (400, 550, 200, 200))
    bsk.draw.line(engine, (255, 255, 255), (100, 50), (600, 300))
    bsk.draw.circle(engine, (255, 255, 0), (200, 600), 100)
    bsk.draw.blit(engine, brick, (100, 200, 200, 200))
    bsk.draw.blit(engine, pg_img, (500, 300, 150, 150))

    engine.update()