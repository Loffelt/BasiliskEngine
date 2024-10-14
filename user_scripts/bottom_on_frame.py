velocity = 15 * delta_time
keys = self.node_handler.scene.engine.keys

dpos = glm.vec3(self.nodes[0].camera.forward.x, 0, self.nodes[0].camera.forward.z) * (keys[pg.K_w] - keys[pg.K_s]) + self.nodes[0].camera.right * (keys[pg.K_d] - keys[pg.K_a])

if glm.length(dpos) > 0: dpos = glm.normalize(dpos)

self.position += dpos * velocity
self.physics_body.velocity += self.nodes[0].camera.UP * velocity * 10 * keys[pg.K_SPACE]

if keys[pg.K_w] or keys[pg.K_s] or keys[pg.K_a] or keys[pg.K_d] or keys[pg.K_SPACE] or keys[pg.K_LSHIFT]: 
    self.physics_body.rotation = glm.angleAxis(glm.radians(self.nodes[0].camera.yaw - 90), self.nodes[0].camera.UP)
    self.physics_body.rotational_velocity = 0