import pymunk
from pymunk import Poly
import game
from drawable import Drawable


class PhysicsBody(Drawable):
    def __init__(self, mesh, shader):
        super().__init__(mesh, shader)

        physics_instance = game.Game.physics_instance

        self.body = pymunk.Body()
        self.body.mass = 0.001
        self.body.position = 0, 0

        self.poly = Poly(self.body, vertices=self.mesh.obj.get_pymunk_vertecies())

        self.poly.mass = 10
        self.poly.friction = 0.62
        physics_instance.space.add(self.body, self.poly)

    def update(self):
        self.position = self.body.position
        self.angle = self.body.angle
