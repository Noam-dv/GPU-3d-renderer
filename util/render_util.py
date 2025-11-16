import numpy as np
import moderngl 
import inspect
import os
#this is lowk just general util not just render util


#------------------------------------------------------------------------------
#general util
#------------------------------------------------------------------------------

def nprint(*args, **kwargs):  
    #help from https://stackoverflow.com/questions/17065086/how-to-get-the-caller-class-name-inside-a-function-of-another-class-in-python
    #costier print functoin that shows line + class name
    #only for debugging

    f = inspect.currentframe().f_back#gets callers frame 
    #thats bascialy just wherer nprint was called
    ln = f.f_lineno #line number

    #getting class name 
    
    if 'self' in f.f_locals:#instance
        classname = f.f_locals['self'].__class__.__name__

    elif 'cls' in f.f_locals:#class
        classname = f.f_locals['cls'].__name__

    else:#not in class for example main or smth
        classname = f.f_globals.get('__name__', '<module>')

    print(f"[{classname}]:[{ln}]:", *args, **kwargs)

#------------------------------------------------------------------------------
#functions to do with shaders
#------------------------------------------------------------------------------

def list_vert_shaders():
    #returns list of vertex shader names without .vert
    l = []
    for f in os.listdir("./shaders/vert"):
        if f.endswith(".vert"):
            l.append(os.path.splitext(f)[0])
    return sorted(l)

def list_frag_shaders():
    #same as last
    l = []
    for f in os.listdir("./shaders/frag"):
        if f.endswith(".frag"):
            l.append(os.path.splitext(f)[0])
    return sorted(l)

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

def default_vertex():
    return get_vert("!")

def default_fragment():
    return get_frag("!")


#------------------------------------------------------------------------------
#functions to do with vertices
#------------------------------------------------------------------------------

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


def add_normals(verts): #calculating normal is essential for lighting
    #https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/geometry-of-a-triangle.html#:~:text=The%20normal%20of%20the%20triangle,in%20a%20counter%2Dclockwise%20manner.
    #basically this function takes a flat array of positions [x,y,z,x,y,z] as triangles
    #it calculates the normal vector for each triangle 
    #and inserts the nromal vec after each point in those trangles in the arr
    verts = np.array(verts, dtype='f4')

    # each triangle is 9 floats: 3 vertices * 3 coords
    if verts.size % 9 == 0:
        nprint("vertex arr must be a mult of 9 (9 verts is 1 triangle)")

    o = []

    #go over each triangle
    #step of 9
    for i in range(0, len(verts), 9):
        p0 = verts[i:i+3]#3 verts of the triangle
        p1 = verts[i+3:i+6]
        p2 = verts[i+6:i+9]
        e1 = p1 - p0 #cross product to get normal vec
        e2 = p2 - p0
        n = np.cross(e1, e2)

        #how far from 0,0,0 is the strength of the vector
        #the angle it make sis the direction
        #we get the normal and divide ny length
        l = np.linalg.norm(n) #we want to preserve the angle but not the strengh of the vector
        #so we divide by the length
        if l != 0:
            n = n / l

        # make new arr with the position and the normal for each vertex

        o.extend(list(p0) + list(n))
        o.extend(list(p1) + list(n))
        o.extend(list(p2) + list(n))

    return np.array(o, dtype='f4')

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


def sphere_verts(radius=1.0, segments=170, rings=80):
    #returns a flat array so we can add normals to it
    verts = []

    for i in range(rings):
        lat0 = np.pi * (-0.5 + float(i) / rings)
        lat1 = np.pi * (-0.5 + float(i + 1) / rings)

        y0 = np.sin(lat0) * radius
        y1 = np.sin(lat1) * radius
        r0 = np.cos(lat0) * radius
        r1 = np.cos(lat1) * radius

        for j in range(segments):
            lon0 = 2 * np.pi * float(j) / segments
            lon1 = 2 * np.pi * float(j + 1) / segments

            x0 = np.cos(lon0)
            z0 = np.sin(lon0)
            x1 = np.cos(lon1)
            z1 = np.sin(lon1)

            #triangle 1
            verts.extend([
                r1 * x1, y1, r1 * z1,
                r0 * x1, y0, r0 * z1,
                r0 * x0, y0, r0 * z0,
            ])

            #triangle 2
            verts.extend([
                r1 * x1, y1, r1 * z1,
                r0 * x0, y0, r0 * z0,
                r1 * x0, y1, r1 * z0,
            ])

    return np.array(verts, dtype='f4')
