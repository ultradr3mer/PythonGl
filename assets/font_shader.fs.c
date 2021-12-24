#version 330

in vec2 v_tex;

uniform sampler2D diffuse_texture;
uniform vec4 color;

out vec4 out_frag_color;

void main() {
	out_frag_color = color;
	out_frag_color.a *= (texture(diffuse_texture,v_tex).r - 0.5) * 1.5 + 0.5;
}