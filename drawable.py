import math

from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

from obj_mtl_loader import Obj


class Drawable:
    boxVerticeBufferId = 0
    boxFaceBufferId = 0

    @staticmethod
    def init():
        Drawable.boxVerticeBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, Drawable.boxVerticeBufferId)
        vertices = np.array([-1, -1, 1, -1, 1, 1, -1, 1], dtype='float32')
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

    def __init__(self, filename=None):
        self.position = (0, 0, 0)
        self.size = (1, 1)
        self.angle = 0
        self.color = (0.5, 0.5, 0.5, 1.0)
        self.verticeBufferId = Drawable.boxVerticeBufferId
        self.drawMode = GL_QUADS
        self.facesBufferId = Drawable.boxFaceBufferId
        self.drawCount = 4
        self.vertexPointerSize = 2
        self.obj: Obj = None

        if isinstance(filename, str):
            self.load_obj(filename)

    def square_from_buffer(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.verticeBufferId)
        glVertexPointer(self.vertexPointerSize, GL_FLOAT, 0, None)
        glColor4f(self.color[0], self.color[1], self.color[2], 0.0)
        glDrawArrays(self.drawMode, 0, self.drawCount)

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.position[0], self.position[1], 0.)
        glScale(self.size[0], self.size[1], 1)
        glRotatef(math.degrees(self.angle), 0.0, 0.0, 1.0)
        self.square_from_buffer()

    def load_obj(self, filename):
        self.obj = Obj(filename)

        self.verticeBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.verticeBufferId)
        vertices = np.array(self.obj.get_plain_vertecies(), dtype='float32')
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        self.drawCount = len(vertices)

        self.drawMode = GL_TRIANGLES
        self.vertexPointerSize = 3


