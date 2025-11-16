import moderngl
import moderngl_window as mglw
import numpy as np
from util.rotation import RotationHandler
from renderer.rendered_object import RenderedObject
from util.render_util import *
class LitRenderedObject(RenderedObject):
    #this class is practically the same as RenderedObject but it passes to the shader the normals
    #needed for lighting
    def __init__(self, ctx, input_vertices, prog=None, position=(0,0,0), camera=None, uniforms = {}, rot_handler=None, rot_intensity=1, auto_normals=True):
        if auto_normals:
            input_vertices = add_normals(input_vertices)

        #if no shader program is passed, use the dedicated lit shader pair
        if prog is None:
            vsrc = get_vert("lit")
            fsrc = get_frag("lit")
            prog = ctx.program(
                vertex_shader=vsrc,
                fragment_shader=fsrc
            )

        super().__init__(
            ctx=ctx,
            input_vertices=input_vertices,
            prog=prog,
            position=position,
            camera=camera,
            uniforms=uniforms,
            rot_handler=rot_handler,
            rot_intensity=rot_intensity
        )

    def load(self):
        self.vertex_buff_obj = self.ctx.buffer(self.input_vertices.astype('f4').tobytes())
        self.vertex_arr_obj = self.ctx.vertex_array(
            self.prog, [ (self.vertex_buff_obj, '3f 3f', 'in_vert', 'in_norm') ] #pass normal vector to get face direction
        )

    def render(self, time, aspect): #old rendering logic but pass all uniforms needed for lighting
        model = self.update(time)
        view = self.camera.view_matrix(self.rot_handler)
        projection = self.camera.projection_matrix(self.rot_handler, aspect)
        mvp = projection @ view @ model

        self.mvp.write(mvp.T.astype('f4').tobytes())

        #itime for shadertoy shaders :-)
        if 'iTime' in self.prog:
            self.prog['iTime'].value = time

        #camera position for lighting just incase if shader uses it
        if hasattr(self.camera, "pos") and 'camPos' in self.prog:
            self.prog['camPos'].value = tuple(self.camera.pos.tolist())

        #model matrix
        if 'modelmat' in self.prog: #we neeed the pass the model matrix to the shader so it can convert from the local space to world space
        #what that means is basically if u check the code
        #verts are computed as 1 0 -1 and numbers that dont actually tell us where they are based on our screen resolution 
        #its object space
        #we need to pass this and the normal mat to convert in_vert and in_norm to world space
            self.prog['modelmat'].write(model.T.astype('f4').tobytes())

        if 'normmat' in self.prog: #normal matrix is used for transforming the in_norm to actual worldspace units insteadof -1 1 0 and shit like that
        #also this is needed for once we trasnform scale and rotate models
        #doesnt replace the in_norms it more like fixes it
            m3 = model[:3, :3]
            normal_mat = np.linalg.inv(m3).T
            self.prog['normmat'].write(normal_mat.astype('f4').tobytes())

        #based color for testing and light src point
        if 'baseCol' in self.prog and 'baseCol' not in self.uniforms:
            self.set_uniform('baseCol', (1.0, 0.0, 1.0))

        if 'lightPos' in self.prog: #point light oribt
            # orbit radius
            r = 6.0
            lx = np.cos(time * 1.2) * r
            ly = 3.0 + np.sin(time * 1.7) * 1.5 
            lz = np.sin(time * 1.2) * r

            light_pos = (lx, ly, lz)
            self.prog['lightPos'].value = light_pos
        if 'l_intensity' in self.prog and 'l_intensity' not in self.uniforms:
            self.set_uniform('l_intensity', 3.0)

        self.vertex_arr_obj.render()
