import pymunk
from pymunk import Poly
import game
from drawable import Drawable


class PhysicsBody(Drawable):
    def __init__(self, mesh, shader, scale):
        super().__init__(mesh, shader)

        physics_instance = game.Game.physics_instance

        self.body = pymunk.Body()
        self.body.mass = 0.001
        self.body.position = 0, 0

        verts = list(map(lambda x: (x[0] * scale, x[1] * scale), self.mesh.obj.get_pymunk_vertecies()))
        self.poly = Poly(self.body, vertices=verts)

        self.poly.mass = 10
        self.poly.friction = 0.7
        physics_instance.space.add(self.body, self.poly)

        self.size = (scale, scale)

    @property
    def position(self):
        return self.body.position

    @position.setter
    def position(self, value):
        self.body.position = value

    @property
    def angle(self):
        return self.body.angle

    @angle.setter
    def angle(self, value):
        self.body.angle = value
