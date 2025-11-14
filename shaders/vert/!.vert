#version 330

in vec3 in_vert; 
uniform mat4 mvp; 
out vec3 v_pos;

void main() {
    gl_Position = mvp * vec4(in_vert, 1.0);
    v_pos = in_vert;
}