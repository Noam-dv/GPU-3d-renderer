import moderngl
import moderngl_window as mglw
from pyrr import Matrix44
import numpy as np
from rotation import RotationHandler
from render_util import default_fragment, default_vertex

class RenderedObject:
    def __init__(self, ctx, input_vertices, prog=None, position=(0,0,0), camera=None, uniforms = {}, rot_handler=None, rot_intensity=1):
        self.input_vertices = input_vertices   

        self.position = np.array(position, dtype='f4')#position saved as a nparray to keep the rowmajor matricse 

        self.camera = camera

        self.vertex_buff_obj=None#passing the points to tgpu 
        #i like to think of it like passing to the stack in assembly
        self.vertex_arr_obj=None#recieveing output

        self.uniforms = uniforms #uniforms saved in dict for checking values for less cost
        self.ctx = ctx
        self.prog = prog #shader program

        self.rot_handler = rot_handler
        if not rot_handler:
            self.rot_handler=RotationHandler()

        self.rot_intensity = rot_intensity

        if not prog:#setup shader program
            self.prog = self.ctx.program(
            vertex_shader=default_vertex(),
            fragment_shader=default_fragment()
        )

        self.mvp = self.prog['mvp'] #save uniform handle
    def set_uniform(self, key, val):
        self.uniforms[key] = val
        if key in self.prog:
            self.prog[key].value = val

    def load(self): 
        self.vertex_buff_obj = self.ctx.buffer(self.input_vertices.astype('f4').tobytes())
        self.vertex_arr_obj = self.ctx.vertex_array(
            self.prog, [(self.vertex_buff_obj, '3f', 'in_vert')] # will be addign an in normal vector so shaders can work differently based on sides
            #rn the frag shader works on each pixel without knowing which way the sphere faces
            #and that issue can cause basically that every pixel that is reused th next frame for the sphere@
            #will generte the same output so the same color
            #so the spheres will look like 2dcircles that arent rotating
            #i hope that makes sense 
        )
            
    def update(self, t):
        rotation = self.rot_handler.rotation_y(t * self.rot_intensity)
        translation = np.eye(4, dtype='f4')
        translation[:3, 3] = self.position
        model = translation @ rotation
        return model
    def set_position(self,pos=(0,0,0)):
        self.position = np.array(pos, dtype='f4')
    def render(self, time, aspect):
        
        model = self.update(time)
        view = self.camera.view_matrix(self.rot_handler)
        projection = self.camera.projection_matrix(self.rot_handler, aspect)
        mvp = projection @ view @ model

        self.mvp.write(mvp.T.astype('f4').tobytes())

        if 'iTime' in self.prog:
            self.prog['iTime'].value = time

        self.vertex_arr_obj.render()