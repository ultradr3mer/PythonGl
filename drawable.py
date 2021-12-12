import math

import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

import game
from mesh import Mesh
from shader import Shader

SIZE_OF_FLOAT32 = 4
SIZE_OF_VEC3_FLOAT = 3 * SIZE_OF_FLOAT32

class Drawable:
    def __init__(self, mesh_filename=None, shader_vert_filename=None, shader_frag_filename=None):
        self.position = (0, 0, 0)
        self.size = (1, 1)
        self.angle = 0
        self.color = (0.5, 0.5, 0.5, 1.0)
        self.verticeBufferId = 0
        self.draw_mode = GL_QUADS
        self.facesBufferId = 0
        self.drawCount = 4
        self.vertexPointerSize = 2
        self.mesh: Mesh = None
        self.shader: Shader = None
        self.vertex_attribute_object = 0
        self.modelview_matrix: glm.mat4 = None

        if isinstance(mesh_filename, str):
            self.load_obj(mesh_filename)

        if isinstance(shader_vert_filename, str) or isinstance(shader_frag_filename, str):
            self.load_shader(shader_vert_filename, shader_frag_filename)

    def square_from_buffer(self):
        glUseProgram(self.shader.shader_program_handle)
        glBindVertexArray(self.vertex_attribute_object)

        self.shader.insert_uniform("projection_matrix", game.Game.projection_matrix)
        self.shader.insert_uniform("modelview_matrix", self.modelview_matrix)
        self.shader.insert_uniform("in_color", self.color)

        glDrawElements(GL_TRIANGLES, self.mesh.indicesCount, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def draw(self):
        self.modelview_matrix = glm.translate(glm.vec3(self.position[0], self.position[1], 0.0))
        self.modelview_matrix = glm.scale(self.modelview_matrix, glm.vec3(self.size[0], self.size[1], 1))
        self.modelview_matrix = glm.rotate(self.modelview_matrix, self.angle, glm.vec3(0.0, 0.0, 1.0))

        # glTranslatef(self.position[0], self.position[1], 0.)
        # glScale(self.size[0], self.size[1], 1)
        # glRotatef(math.degrees(self.angle), 0.0, 0.0, 1.0)
        self.square_from_buffer()

        # glUseProgram(self.shader.shader_program_handle)
        # glBindVertexArray(self.vertex_attribute_object)
        # glDrawElements(self.draw_mode, self.mesh.indicesCount, GL_UNSIGNED_INT, 0)

    def load_obj(self, filename):
        self.mesh = Mesh(filename)
        self.draw_mode = GL_TRIANGLES
        self.vertexPointerSize = 3

    def load_shader(self, shader_vert_filename, shader_frag_filename):
        self.shader = Shader(shader_vert_filename, shader_frag_filename)
        self.vertex_attribute_object = self.shader.create_vertex_attribute_object(self.mesh)
