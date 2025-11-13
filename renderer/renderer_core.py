import numpy as np
import moderngl
from renderer.rendered_object import RenderedObject
from rotation import RotationHandler
from render_util import *
from spacetime import RenderedSpacetime
from camera import Camera

class RendererCore:
    #windowconfig is removed so pygame can use this renderrer too 
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx

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
        with open("./shaders/stolen shadertoy shader 1.frag", "r") as s:
            raw_shader=s.read()

        p_fire = self.ctx.program(
            vertex_shader = default_vertex(), #ported shader from here https://www.shadertoy.com/view/MlKSWm
            fragment_shader=raw_shader 
        )

        with open("./shaders/stolen shadertoy shader 2.frag", "r") as s:
            raw_shader=s.read()

        p_cool = self.ctx.program(
            vertex_shader = default_vertex(), #ported shader from here https://www.shadertoy.com/view/MlKSWm
            fragment_shader=raw_shader 
        ) 

        self.rendered_objects = [
            RenderedSpacetime(ctx=self.ctx, size=10, blocks=30, camera=self.camera, rot_handler=self.rot),
            RenderedObject(ctx=self.ctx, input_vertices=cube_verts(), prog=p_fire, position=(0,0,0), camera=self.camera, rot_handler=self.rot, rot_intensity=0)
        ]
        self.rendered_objects[0].set_uniform("time", 0.0) #initialize incase it has
        
        for i in self.rendered_objects:
            i.load()

    def test_orbit(self, time, r=5.0, s=0.3, y=2.0):
        x=np.sin(time * s) * r 
        z=np.cos(time * s) * r
        self.camera.set_position((x, y, z))

    def render(self, time, aspect):
        self.ctx.clear(0., 0., 0., 1.0)

        #test cam movement
        self.test_orbit(time)

        for i in range(len(self.rendered_objects)):
            self.rendered_objects[i].render(time, aspect)