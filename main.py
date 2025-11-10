import moderngl
import moderngl_window as mglw
from pyrr import Matrix44
import numpy as np
from rotation import RotationHandler
from constants import *

class Renderer(mglw.WindowConfig):
    gl_version = (3,3)
    title = "gpu 3d renderer"
    window_size = (800,600)
    resource_dir = '.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rot = RotationHandler()

        verts = np.array([#basic triangle vertices
            -1.0, -1.0, 0.0, #. 
            1.0, -1.0, 0.0,  #      .
            0.0,  1.0, 0.0,  #   .
        ], dtype='f4')

        #those points combined by lines makes something like this 
        #.  .  .
        # . . .
        #   . 
        #wait i did that triangle drawing perfectly tahats crazy

        # ensure float32 tightly-packed data
        self.vertex_buff_obj = self.ctx.buffer(cube_verts().astype('f4').tobytes()) #writing full variabel names so i can learn and remember better
        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec3 in_vert;
                uniform mat4 mvp;
                void main() {
                    gl_Position = mvp * vec4(in_vert, 1.0);
                }
            ''',
            fragment_shader='''
            #version 330

            out vec4 fragColor;
            in vec4 gl_FragCoord;

            uniform float iTime;

            float hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
            }

            float noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                vec2 u = f * f * (3.0 - 2.0 * f);
                return mix(
                    mix(hash(i + vec2(0.0, 0.0)), hash(i + vec2(1.0, 0.0)), u.x),
                    mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x),
                    u.y
                );
            }
            void main() {
                vec2 uv = gl_FragCoord.xy / vec2(800.0, 600.0);
                fragColor = vec4(uv, 1.0, 1.0);
            }
            '''

        )
        self.time_uniform = self.prog.get('iTime', None)

        self.mvp = self.prog['mvp'] #get uniform handle

        self.vertex_arr_obj = self.ctx.vertex_array(self.prog, [(self.vertex_buff_obj, '3f', 'in_vert')])
    
    def on_render(self, time, frame_time):
        self.ctx.clear(0, 0, 0, 1.0)
        if self.time_uniform:
            self.time_uniform.value = time

        model = self.rot.rotation_y(time)
        eye = (0,np.sin(time) * 2,5) #cam pos
        target = (0,0,0) #where cam should be pointed
        up = (0,1,0) #which way is up
        #used to determine cam angle

        view = self.rot.look_at(eye, target, up)

        #use the real window aspect ratio
        aspect = self.wnd.aspect_ratio
        projection = self.rot.perspective(45.0, aspect, 0.1, 100.0)

        x = projection @ view @ model
        #transpose to colum nmajor for GLSL
        self.mvp.write(x.T.astype("f4").tobytes()) #send x to gpu as bytes
        self.vertex_arr_obj.render()#render triangle

if __name__ == "__main__":
    mglw.run_window_config(Renderer)
