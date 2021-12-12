from typing import Tuple

import glm
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

SIZE_OF_FLOAT32 = 4
SIZE_OF_VEC3_FLOAT = 3 * SIZE_OF_FLOAT32


class Shader:
    def __init__(self, vertex_file, fragment_file):
        vertex_shader_handle = glCreateShader(GL_VERTEX_SHADER)
        fragment_shader_handle = glCreateShader(GL_FRAGMENT_SHADER)

        with open(vertex_file, "r") as f:
            content = f.read()
            glShaderSource(vertex_shader_handle, content)

        with open(fragment_file, "r") as f:
            content = f.read()
            glShaderSource(fragment_shader_handle, content)

        glCompileShader(vertex_shader_handle)
        if glGetError() != 0:
            raise Exception(glGetShaderInfoLog(vertex_shader_handle))

        glCompileShader(fragment_shader_handle)
        if glGetError() != 0:
            raise Exception(glGetShaderInfoLog(fragment_shader_handle))

        shader_program_handle = glCreateProgram()

        glAttachShader(shader_program_handle, vertex_shader_handle)
        glAttachShader(shader_program_handle, fragment_shader_handle)

        glLinkProgram(shader_program_handle)

        self.shader_program_handle = shader_program_handle

    def create_vertex_attribute_object(self, mesh):
        vao_handle = glGenVertexArrays(1)
        glBindVertexArray(vao_handle)

        # normal_index = glGetAttribLocation(self.shader_program_handle, "in_normal")
        position_index = glGetAttribLocation(self.shader_program_handle, "in_position")
        # tangent_index = glGetAttribLocation(self.shader_program_handle, "in_tangent")
        # texture_index = glGetAttribLocation(self.shader_program_handle, "in_texture")

        if position_index != -1:
            glEnableVertexAttribArray(position_index)
            glBindBuffer(GL_ARRAY_BUFFER, mesh.verticeBufferId)
            glVertexAttribPointer(position_index, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.indexBufferId)

        glBindVertexArray(0)

        return vao_handle

    def insert_uniform(self, uniform_name, value):
        location = glGetUniformLocation(self.shader_program_handle, uniform_name)

        if isinstance(value, glm.mat4):
            glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(value))
            return

        if isinstance(value, tuple):
            if len(value) == 4:
                glUniform4fv(location, 1, arrays.GLfloatArray(value))
                return

