#version 330

uniform vec4 in_color;

out vec4 out_frag_color;

void main() {
	out_frag_color = in_color;
}