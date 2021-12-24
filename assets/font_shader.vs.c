#version 330

uniform mat4 modelview_matrix;
uniform mat4 projection_matrix;

in vec3 in_position;
in vec2 in_texture;

out vec2 v_tex;

void main(void)
{
    v_tex = in_texture;
	gl_Position = projection_matrix * modelview_matrix * vec4(in_position, 1);
}