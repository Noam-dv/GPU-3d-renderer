#version 330 core

in vec3 iNorm;
in vec3 iWorldpos;

uniform vec3 lightPos; //not world space remember
uniform vec3 camPos;
uniform vec3 baseCol;
uniform float l_intensity;

out vec4 fragColor;

void main() {
    vec3 norm = normalize(iNorm);
    vec3 lp = normalize(lightPos-iWorldpos);
    vec3 view = normalize(camPos-iWorldpos);

    float diff = max(dot(norm, lp), 0.0);

    vec3 h = normalize(lp + view);
    float spec = pow(max(dot(norm, h), 0.0), 64.0);

    float d = length(lightPos - iWorldpos);
    float att = 1.0 / (1.0 + 0.1* (d*d));

    vec3 c = (baseCol*diff + spec*0.5) *att *l_intensity;
    c += vec3(0.05);//offset for ambient light 
    fragColor = vec4(c, 1.0);
}
