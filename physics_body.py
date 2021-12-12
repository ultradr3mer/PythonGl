import math

import pymunk
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from pymunk import Poly

import game
from drawable import Drawable


class PhysicsBody(Drawable):
    def __init__(self, filename=None):
        super().__init__(filename)

        physics_instance = game.Game.physics_instance

        self.body = pymunk.Body()
        self.body.mass = 0.001
        self.body.position = 0, 0

        self.poly = Poly(self.body, vertices=self.obj.get_pymunk_vertecies())

        self.poly.mass = 10
        self.poly.friction = 0.62
        physics_instance.space.add(self.body, self.poly)

    def update(self):
        self.position = self.body.position
        self.angle = self.body.angle
