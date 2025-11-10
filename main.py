import moderngl
import moderngl_window as mglw
from pyrr import Matrix44
import numpy as np
from rotation import RotationHandler
from constants import *

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
        self.vertex_arr_obj = self.ctx.vertex_array(self.prog, [(self.vertex_buff_obj, '3f', 'in_vert')])
    
    def update(self, t):
        rotation = self.rot_handler.rotation_y(t * self.rot_intensity)
        translation = np.eye(4, dtype='f4')
        translation[:3, 3] = self.position
        model = rotation @ translation
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
            RenderedObject(ctx=self.ctx, input_vertices=sphere_verts(), prog=p_fire, position=(-1,0,0), camera=self.camera, rot_handler=self.rot, rot_intensity=2),
            RenderedObject(ctx=self.ctx, input_vertices=cube_verts(), prog=p_cool, position=(1,0,0), camera=self.camera, rot_handler=self.rot, rot_intensity=2)
        ]
        self.rendered_objects[0].set_uniform("time", 0.0)
        
        for i in self.rendered_objects:
            i.load()

    
    def on_render(self, time, frame_time):
        self.ctx.clear(0.45, 0., 0.7, 1.0)
        #self.camera.set_position((0,0,5+np.sin(time))) js a test for cam movement

        aspect = self.wnd.aspect_ratio
        for i in range(len(self.rendered_objects)):
            self.rendered_objects[i].render(time,aspect)
if __name__ == "__main__":
    mglw.run_window_config(Renderer)
