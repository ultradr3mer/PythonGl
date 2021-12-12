#version 330

in vec2 v_tex;

uniform sampler2D diffuse_texture;

out vec4 out_frag_color;

void main() {
	out_frag_color = texture(diffuse_texture,v_tex);
}