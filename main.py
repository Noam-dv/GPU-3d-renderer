import moderngl
import moderngl_window as mglw
from pyrr import Matrix44
import numpy as np
from rendered_object import RenderedObject
from rotation import RotationHandler
from render_util import *
from spacetime import RenderedSpacetime
class Camera:
    def __init__(self, eye=(0,0,5), target=(0,0,0), up=(0,1,0)):
        self.pos = np.array(eye, dtype='f4')
        self.target = np.array(target, dtype='f4')
        self.up = np.array(up, dtype='f4')

    def set_position(self, pos):
        self.pos = np.array(pos, dtype='f4')

    def view_matrix(self, rot_handler):
        return rot_handler.look_at(self.pos, self.target, self.up)

    def projection_matrix(self, rot_handler, aspect):
        return rot_handler.perspective(45.0, aspect, 0.1, 100.0)
    

class Renderer(mglw.WindowConfig):
    gl_version = (3,3)
    title = "gpu 3d renderer"
    window_size = (800,600)
    resource_dir = '.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        verts = np.array([#basic triangle vertices
            -1.0, -1.0, 0.0, #. 
            1.0, -1.0, 0.0,  #      .
            0.0,  1.0, 0.0,  #   .
        ], dtype='f4')#those points combined by lines makes something like this 
        #.  .  .
        # . . .
        #   . 
        #wait i did that triangle drawing perfectly tahats crazy
        self.rot = RotationHandler()
        self.camera = Camera(eye=(0,2,5),target=(0,0,0),up=(0,1,0))

        self.raw_shader=""
        with open("stolen shadertoy shader 1.frag", "r") as s:
            raw_shader=s.read()

        p_fire = self.ctx.program(
            vertex_shader = default_vertex(), #ported shader from here https://www.shadertoy.com/view/MlKSWm
            fragment_shader=raw_shader 
        )

        with open("stolen shadertoy shader 2.frag", "r") as s:
            raw_shader=s.read()

        p_cool = self.ctx.program(
            vertex_shader = default_vertex(), #ported shader from here https://www.shadertoy.com/view/MlKSWm
            fragment_shader=raw_shader 
        ) 

        self.rendered_objects = [
            RenderedSpacetime(ctx=self.ctx, size=10, blocks=30, camera=self.camera, rot_handler=self.rot),
            RenderedObject(ctx=self.ctx, input_vertices=cube_verts(), prog=p_cool, position=(0,0,0), camera=self.camera, rot_handler=self.rot, rot_intensity=0)
        ]
        self.rendered_objects[0].set_uniform("time", 0.0)
        
        for i in self.rendered_objects:
            i.load()

    def test_orbit(self, time, r=5.0, s=0.3, y=2.0):
        x=np.sin(time * s) * r 
        z=np.cos(time * s) * r
        self.camera.set_position((x, y, z))
    def on_render(self, time, frame_time):
        self.ctx.clear(0., 0., 0., 1.0)
        #self.camera.set_position((0,0,5+np.sin(time))) js a test for cam movement

        self.test_orbit(time)

        aspect = self.wnd.aspect_ratio
        for i in range(len(self.rendered_objects)):
            self.rendered_objects[i].render(time,aspect)
if __name__ == "__main__":
    mglw.run_window_config(Renderer)
