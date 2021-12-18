import numpy as np
from OpenGL.GL import *


class GenMesh:
    def __init__(self):
        self.verticeBufferId = glGenBuffers(1)
        self.textureCoordBufferId = glGenBuffers(1)
        self.length = 0

    def update(self, verts, tex_coords):

        if verts:
            glBindBuffer(GL_ARRAY_BUFFER, self.verticeBufferId)
            vertices = np.array(verts, dtype='float32')
            glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
            self.length = len(vertices) * 3

        if tex_coords:
            glBindBuffer(GL_ARRAY_BUFFER, self.textureCoordBufferId)
            coords = np.array(tex_coords, dtype='float32')
            glBufferData(GL_ARRAY_BUFFER, coords, GL_STATIC_DRAW)
