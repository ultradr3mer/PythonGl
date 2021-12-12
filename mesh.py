import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from obj_loader import Obj

class Mesh:
    def __init__(self, filename):
        self.obj = Obj(filename)

        self.verticeBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.verticeBufferId)
        vertices = np.array(self.obj.plain_vertecies, dtype='float32')
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        self.length = len(vertices) * 3

        self.textureCoordBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.textureCoordBufferId)
        coords = np.array(self.obj.plain_texcoords, dtype='float32')
        glBufferData(GL_ARRAY_BUFFER, coords, GL_STATIC_DRAW)
