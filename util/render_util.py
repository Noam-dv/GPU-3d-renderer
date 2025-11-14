import numpy as np
import moderngl 

def get_frag(src):
    r=""
    with open("./shaders/frag/" + src + ".frag", "r") as s:
        r=s.read()
    return r

def get_vert(src):
    r=""
    with open("./shaders/vert/" + src + ".vert", "r") as s:
        r=s.read()
    return r

def centered_flatgrid(s=10, b=50):#CORRECTED GRID LINE CODE!!!! 
    verts = []
    step = s/b #size divided by how many blocks we want

    #vertical lines
    for i in range(b + 1):
        #-size/2 ------- 0.0 --------size/2--------- size 
        #-size/2 basically js centers everything proportiortinlaly how do u even spell that word 
        x = -s/2 + i * step
        verts += [x, 0, -s/2,  x, 0, s/2]

    #horiz lines
    for i in range(b + 1):
        z = -s/2 + i * step
        verts += [-s/2, 0, z,  s/2, 0, z]

    return np.array(verts, dtype='f4')

# DIDNT WORK :-)
# def centered_flatgrid(s, b): #overall size and grid block size 
#     step = s/b
#     verts = []
#     startpoint = -s/2 #itd be like 
#     #startpoint     0.0               size      
#     # so u split it in half and minus it so its centered   
#     for i in range(s):
#         for j in range(s):
#             x0 = startpoint + i*step
#             z0 = startpoint + j*step
#             x1 = x0 + step
#             z1 = z0 + step

#             #each suqare is 2 triangles
#             #so we make 2 triangles 
#             #one from x0 z0 ------- x1 z0  (i tried my best to visuzlie this)
#             #                          |
#             #                          |
#             #                          |
#             #                       x1 z1
#             # Tthen do the same with the other triangle
#             #this isnt exactly correct cuz order matters in opengl, but its the premise

#             #(the 0s are y)
#             verts += [x0,0,z0,  x1,0,z0,  x1,0,z1]
#             verts += [x0,0,z0,  x1,0,z1,  x0,0,z1]
#     return np.array(verts,dtype=np.float32)

def default_vertex(): #wavy shader test
    return '''
        #version 330

        in vec3 in_vert; 
        uniform mat4 mvp; 
        out vec3 v_pos;

        void main() {
            gl_Position = mvp * vec4(in_vert, 1.0);
            v_pos = in_vert;
        }

    '''

def default_fragment():
    return '''
            #version 330


            in vec3 v_pos;
            out vec4 fragColor;

            void main() {
                vec3 color = 0.5 + 0.5 * normalize(v_pos);
                fragColor = vec4(color, 1.0);
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
