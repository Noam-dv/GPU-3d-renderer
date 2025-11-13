import numpy as np
from renderer.rendered_object import RenderedObject
from render_util import centered_flatgrid,default_vertex,default_fragment
import moderngl 

class RenderedSpacetime(RenderedObject):
    def __init__(self, ctx, size=10, blocks=50, camera=None, rot_handler=None):
        #grid lines from renderutil
        input_vertices = centered_flatgrid(size, blocks)

        #use custom shader
        prog = ctx.program(vertex_shader=default_vertex(), fragment_shader=default_fragment())

        super().__init__( #nto writing all tgat again
            ctx=ctx,
            input_vertices=input_vertices,
            prog=prog,
            position=(0, -1, 0),
            camera=camera,
            rot_handler=rot_handler,
            rot_intensity=0
        )
        
    def render(self, time, aspect):#override render with the line rendering
        model = self.update(time)# all the old rendering logic
        view = self.camera.view_matrix(self.rot_handler)
        projection = self.camera.projection_matrix(self.rot_handler, aspect)
        mvp = projection @ view @ model

        self.mvp.write(mvp.T.astype('f4').tobytes())

        if 'iTime' in self.prog: #kept for spacetime grid incase i wanna add interactive shaders on it :) (maybe for fading)
            self.prog['iTime'].value = time

        self.vertex_arr_obj.render(mode=moderngl.LINES)#draw grid lines instead of fillig in the triangles
        #old method basically just draws a plane because it missed this one line of code 😁👌
