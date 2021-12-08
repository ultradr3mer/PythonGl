import math

import pymunk
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import game


class Drawable:
    verticeBufferId = 0

    @staticmethod
    def init():
        Drawable.verticeBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, Drawable.verticeBufferId)
        vertices = np.array([-1, -1, 1, -1, 1, 1, -1, 1], dtype='float32')
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

    def __init__(self):
        physics_instance = game.Game.physics_instance

        self.body = pymunk.Body()
        self.body.mass = 0.001
        self.body.position = 0, 0

        self.poly = pymunk.Poly.create_box(self.body, size=(2, 2))
        self.poly.mass = 10
        self.poly.friction = 0.62
        physics_instance.space.add(self.body, self.poly)

    @staticmethod
    def square_from_buffer():
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, Drawable.verticeBufferId)
        glVertexPointer(2, GL_FLOAT, 0, None)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glDrawArrays(GL_QUADS, 0, 4)

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        pos = self.body.position
        glTranslatef(pos.x, pos.y, 0.0)
        rotation = math.degrees(self.body.angle)
        glRotatef(rotation, 0.0, 0.0, 1.0)
        glColor3f(1.0, 0.0, 3.0)
        Drawable.square_from_buffer()

    @property
    def position(self):
        return self.body.position

    @position.setter
    def position(self, value):
        self.body.position = value
        pass

