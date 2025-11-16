#version 330 core

in vec3 in_vert;
in vec3 in_norm;

uniform mat4 mvp;
uniform mat4 modelmat;
uniform mat3 normmat;

out vec3 iNorm;
out vec3 iWorldpos;

void main() {
    vec4 pos = modelmat * vec4(in_vert, 1.0); //thisis the conversion to worldpos
    iWorldpos = pos.xyz;
    iNorm = normalize(normmat * in_norm);
    gl_Position = mvp * vec4(in_vert, 1.0);
}
