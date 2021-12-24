import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
import game
from tex import Tex


class Drawable:
    def __init__(self, mesh, shader):
        self._position = (0, 0, 0)
        self.size = (1, 1)
        self._angle = 0
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.verticeBufferId = 0
        self.mesh = mesh
        self.shader = shader
        self.vertex_attribute_object = 0
        self.modelview_matrix: glm.mat4 = None

        self.vertex_attribute_object = self.shader.create_vertex_attribute_object(self.mesh)

        self._textures: list[Tex] = list()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def draw(self):
        self.modelview_matrix = glm.translate(glm.vec3(self.position[0], self.position[1], 0.0))
        self.modelview_matrix = glm.scale(self.modelview_matrix, glm.vec3(self.size[0], self.size[1], 1))
        self.modelview_matrix = glm.rotate(self.modelview_matrix, self.angle, glm.vec3(0.0, 0.0, 1.0))

        glUseProgram(self.shader.shader_program_handle)

        tex_id = 0
        for tex in self._textures:
            glActiveTexture(GL_TEXTURE0 + tex_id)
            glBindTexture(GL_TEXTURE_2D, tex.handle)
            # glUniform1(GL.GetUniformLocation(handle, target + (i + 1)), i);

        glBindVertexArray(self.vertex_attribute_object)

        self.shader.insert_uniform("projection_matrix", game.Game.projection_matrix)
        self.shader.insert_uniform("modelview_matrix", self.modelview_matrix)
        self.shader.insert_uniform("color", self.color)

        glDrawArrays(GL_TRIANGLES, 0, self.mesh.length)
        glBindVertexArray(0)

    def add_tex(self, additional_tex):
        self._textures.append(additional_tex)
