import numpy as np
#thanks chatgpt 

def cube_verts():
    # cube centered at origin triangles
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
