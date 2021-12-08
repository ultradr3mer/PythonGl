import math

from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np


class Drawable:
    verticeBufferId = 0

    @staticmethod
    def init():
        Drawable.verticeBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, Drawable.verticeBufferId)
        vertices = np.array([-1, -1, 1, -1, 1, 1, -1, 1], dtype='float32')
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

    def __init__(self):
        self._position = (0, 0, 0)
        self.size = (1, 1)
        self.angle = 0
        self.color = (0.5, 0.5, 0.5, 1.0)

    def square_from_buffer(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, Drawable.verticeBufferId)
        glVertexPointer(2, GL_FLOAT, 0, None)
        glColor4f(self.color[0], self.color[1], self.color[2], 0.0)
        glDrawArrays(GL_QUADS, 0, 4)

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.position[0], self.position[1], 0.)
        glScale(self.size[0], self.size[1], 1)
        glRotatef(math.degrees(self.angle), 0.0, 0.0, 1.0)
        self.square_from_buffer()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        pass

