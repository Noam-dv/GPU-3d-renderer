from scenes.scene import Scene
import numpy as np
import moderngl
from renderer.rendered_object import RenderedObject
from util.render_util import *
from objects.spacetime import RenderedSpacetime

class STest(Scene):
    #this is the originla scene moved out of renderer core and instead put here for organization
    def __init__(self, ctx: moderngl.Context, camera, rot_handler):
        super().__init__()

        verts = np.array([#basic triangle vertices
            -1.0, -1.0, 0.0, #. 
            1.0, -1.0, 0.0,  #      .
            0.0,  1.0, 0.0,  #   .
        ], dtype='f4')#those points combined by lines makes something like this 
        #.  .  .
        # . . .
        #   . 
        #wait i did that triangle drawing perfectly tahats crazy

        p_fire = ctx.program(
            vertex_shader = default_vertex(), #ported shader from here https://www.shadertoy.com/view/MlKSWm
            fragment_shader=get_frag("stolen shadertoy shader 1") 
        )

        p_cool = ctx.program(
            vertex_shader = default_vertex(), #ported shader from here https://www.shadertoy.com/view/MlKSWm
            fragment_shader=get_frag("stolen shadertoy shader 2") 
        ) 

        spacetime = RenderedSpacetime(ctx=ctx, size=10, blocks=30, camera=camera, rot_handler=rot_handler)
        spacetime.set_uniform("time", 0.0) #initialize incase it has
        
        cube = RenderedObject(ctx=ctx, input_vertices=cube_verts(), prog=p_cool, position=(0,0,0), camera=camera, rot_handler=rot_handler, rot_intensity=0)

        self.objects = [ #these will all be rendered
            spacetime,
            cube
        ]