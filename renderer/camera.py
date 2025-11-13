import numpy as np

class Camera:#basic ass camera
    def __init__(self, eye=(0,0,5), target=(0,0,0), up=(0,1,0)):
        self.pos = np.array(eye, dtype='f4')
        self.target = np.array(target, dtype='f4')
        self.up = np.array(up, dtype='f4')#true up vectoir for renderer to know which way is up relative to teh actual world

    def set_position(self, pos):
        self.pos = np.array(pos, dtype='f4')

    def view_matrix(self, rot_handler):
        return rot_handler.look_at(self.pos, self.target, self.up)

    def projection_matrix(self, rot_handler, aspect):
        return rot_handler.perspective(45.0, aspect, 0.1, 100.0)