import numpy as np

class RotationHandler():
    #math helper functions, all are common functions for 3d rendering, none of the logic is actually made by me

    def __init__(self):
        print("rotation handler initialized")
    
    @staticmethod 
    def rotation_y(t): #rotation matrix for y
        c = np.cos(t)
        s = np.sin(t)
        return np.array([
            [ c, 0,  s, 0],
            [ 0, 1,  0, 0],
            [-s, 0,  c, 0],
            [ 0, 0,  0, 1]
        ], dtype=np.float32)

    @staticmethod
    def look_at(eye, target, up): #common look at algorithm
        eye = np.array(eye, dtype=np.float32)
        target = np.array(target, dtype=np.float32)
        up = np.array(up, dtype=np.float32)

        f = target - eye #position urself at target looking atr position - the cameras position
        f = f / np.linalg.norm(f)
        r = np.cross(f, up) #find right direction
        r = r / np.linalg.norm(r)
        u = np.cross(r, f)#find up direction to determine angle

        mat = np.eye(4, dtype=np.float32)
        mat[0, :3] = r
        mat[1, :3] = u
        mat[2, :3] = -f
        mat[:3, 3] = -np.dot(mat[:3, :3], eye)
        return mat

    @staticmethod
    def perspective(fov_deg, aspect, near, far): #converts 3d points into 2d projected screen positions based on depth
        f = 1.0 / np.tan(np.radians(fov_deg) / 2.0)#i dont understand this one at all so i cant leave comments
        P = np.zeros((4, 4), dtype=np.float32)
        P[0, 0] = f / aspect
        P[1, 1] = f
        P[2, 2] = (far + near) / (near - far)
        P[2, 3] = (2.0 * far * near) / (near - far)
        P[3, 2] = -1.0
        P[3, 3] = 0.0
        return P