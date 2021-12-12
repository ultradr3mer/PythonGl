import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
import game


class Drawable:
    def __init__(self, mesh, shader):
        self.position = (0, 0, 0)
        self.size = (1, 1)
        self.angle = 0
        self.color = (0.5, 0.5, 0.5, 1.0)
        self.verticeBufferId = 0
        self.mesh = mesh
        self.shader = shader
        self.vertex_attribute_object = 0
        self.modelview_matrix: glm.mat4 = None

        self.vertex_attribute_object = self.shader.create_vertex_attribute_object(self.mesh)

    def draw(self):
        self.modelview_matrix = glm.translate(glm.vec3(self.position[0], self.position[1], 0.0))
        self.modelview_matrix = glm.scale(self.modelview_matrix, glm.vec3(self.size[0], self.size[1], 1))
        self.modelview_matrix = glm.rotate(self.modelview_matrix, self.angle, glm.vec3(0.0, 0.0, 1.0))

        glUseProgram(self.shader.shader_program_handle)
        glBindVertexArray(self.vertex_attribute_object)

        self.shader.insert_uniform("projection_matrix", game.Game.projection_matrix)
        self.shader.insert_uniform("modelview_matrix", self.modelview_matrix)
        self.shader.insert_uniform("in_color", self.color)

        glDrawElements(GL_TRIANGLES, self.mesh.indicesCount, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

