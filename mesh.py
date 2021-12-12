import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from obj_mtl_loader import Obj

SIZE_OF_FLOAT32 = 4
SIZE_OF_VEC3_FLOAT = 3 * SIZE_OF_FLOAT32

class Mesh:
    def __init__(self, filename):
        self.obj = Obj(filename)

        self.verticeBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.verticeBufferId)
        vertices = np.array(self.obj.get_vertecies(), dtype='float32')
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

        self.indexBufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.indexBufferId)
        indices = np.array(self.obj.get_indices(), dtype='intc')
        glBufferData(GL_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
        self.indicesCount = len(indices)


