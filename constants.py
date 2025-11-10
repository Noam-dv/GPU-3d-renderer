import numpy as np
import moderngl 
def default_vertex(): #wavy shader test
    return '''
    #version 330
    in vec3 in_vert;

    uniform mat4 mvp;
    uniform float time;
    out vec3 in_vert_out;

    void main() {
        float wave = sin(in_vert.x * 2.0 + time * 1.2) * 0.1 +
                     cos(in_vert.y * 3.0 + time * 0.8) * 0.1;

        vec3 displaced = in_vert + vec3(0.0, wave, 0.0);
        gl_Position = mvp * vec4(displaced, 1.0);
        in_vert_out = displaced;
    }
    '''

def default_fragment():
    return '''
            #version 330

            out vec4 fragColor;
            in vec4 gl_FragCoord;

            uniform float iTime;

            float hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
            }

            float noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                vec2 u = f * f * (3.0 - 2.0 * f);
                return mix(
                    mix(hash(i + vec2(0.0, 0.0)), hash(i + vec2(1.0, 0.0)), u.x),
                    mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x),
                    u.y
                );
            }
            void main() {
                vec2 uv = gl_FragCoord.xy / vec2(800.0, 600.0);
                fragColor = vec4(uv, 1.0, 1.0);
            }
            '''
def cube_verts():
    # cube centered at origin triangles (thanks chatgpt)
    v = [
        -1,-1, 1,  1,-1, 1,  1, 1, 1,
        -1,-1, 1,  1, 1, 1, -1, 1, 1,
        -1,-1,-1, -1, 1,-1,  1, 1,-1,
        -1,-1,-1,  1, 1,-1,  1,-1,-1,
         1,-1,-1,  1, 1,-1,  1, 1, 1,
         1,-1,-1,  1, 1, 1,  1,-1, 1,
        -1,-1,-1, -1,-1, 1, -1, 1, 1,
        -1,-1,-1, -1, 1, 1, -1, 1,-1,
        -1, 1,-1, -1, 1, 1,  1, 1, 1,
        -1, 1,-1,  1, 1, 1,  1, 1,-1,
        -1,-1,-1,  1,-1,-1,  1,-1, 1,
        -1,-1,-1,  1,-1, 1, -1,-1, 1,
    ]
    return np.array(v, dtype=np.float32)


def sphere_verts(radius=1.0, segments=32, rings=16):
    vertices = []
    for i in range(rings):
        lat0 = np.pi * (-0.5 + float(i) / rings)
        lat1 = np.pi * (-0.5 + float(i + 1) / rings)

        y0 = np.sin(lat0)
        y1 = np.sin(lat1)
        r0 = np.cos(lat0)
        r1 = np.cos(lat1)

        for j in range(segments):
            lon0 = 2 * np.pi * float(j) / segments
            lon1 = 2 * np.pi * float(j + 1) / segments

            x0 = np.cos(lon0)
            z0 = np.sin(lon0)
            x1 = np.cos(lon1)
            z1 = np.sin(lon1)

            vertices.extend([
                [r1 * x1 * radius, y1 * radius, r1 * z1 * radius],
                [r0 * x1 * radius, y0 * radius, r0 * z1 * radius],
                [r0 * x0 * radius, y0 * radius, r0 * z0 * radius],

                [r1 * x1 * radius, y1 * radius, r1 * z1 * radius],
                [r0 * x0 * radius, y0 * radius, r0 * z0 * radius],
                [r1 * x0 * radius, y1 * radius, r1 * z0 * radius],
            ])
    return np.array(vertices, dtype=np.float32)
