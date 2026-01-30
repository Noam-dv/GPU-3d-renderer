import numpy as np

class Camera:
    """simple camera based off every other 3d camera in existence"""
    def __init__(self, eye=(0,0,5), target=(0,0,0), up=(0,1,0)):
        self.pos = np.array(eye, dtype='f4')
        self.target = np.array(target, dtype='f4')
        self.up = np.array(up, dtype='f4') #true up vector for renderer to know which way is up relative to the actual world

    """ simple helpers plus transforms """
    def set_position(self, pos):
        self.pos = np.array(pos, dtype='f4')

    def view_matrix(self, rot_handler):
        return rot_handler.look_at(self.pos, self.target, self.up)

    def projection_matrix(self, rot_handler, aspect):
        return rot_handler.perspective(45.0, aspect, 0.1, 100.0)
