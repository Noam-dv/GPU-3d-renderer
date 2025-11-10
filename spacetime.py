import numpy as np
from rendered_object import RenderedObject
from render_util import centered_flatgrid
import moderngl 

class RenderedSpacetime(RenderedObject):
    def __init__(self, ctx, size=10, blocks=50, camera=None, rot_handler=None):
        #grid lines from renderutil
        input_vertices = centered_flatgrid(size, blocks)

        #use custom shader
        prog = ctx.program(vertex_shader=self.vertex_shader(), fragment_shader=self.fragment_shader())

        super().__init__( #nto writing all tgat again
            ctx=ctx,
            input_vertices=input_vertices,
            prog=prog,
            position=(0, -1, 0),
            camera=camera,
            rot_handler=rot_handler,
            rot_intensity=0
        )

    def vertex_shader(self): 
        #small warping shader for making the grid interact with the rendered objs
        return '''
        #version 330
        in vec3 in_vert;
        uniform mat4 mvp;
        uniform float iTime;

        out vec3 v_pos; // pass position for coloring

        void main() {
            vec3 pos = in_vert;

            // simple pulsing heightwave for test, remove later
            pos.y += 0.02 * sin(iTime * 2.0 + length(pos.xz) * 10.0);

            v_pos = pos;
            gl_Position = mvp * vec4(pos, 1.0);
        }
        '''

    def fragment_shader(self): #simple glowing shader for the gird
        return '''
        #version 330
        in vec3 v_pos;
        out vec4 fragColor;
        uniform float iTime;

        void main() {
            // smooth glowing cyan-blue grid
            float brightness = 0.6 + 0.4 * sin(iTime * 1.5);
            vec3 baseColor = vec3(0.2, 0.9, 1.0);

            // fade lines slightly toward the horizon
            float falloff = clamp(1.0 - abs(v_pos.y) * 3.0, 0.0, 1.0);

            // final blended color
            vec3 color = baseColor * brightness * falloff;
            fragColor = vec4(color, 1.0);
        }
        '''

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
