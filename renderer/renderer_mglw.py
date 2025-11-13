import moderngl_window as mglw
from renderer.renderer_core import RendererCore
#this is the renderer if werre using a modernglwindow 
#wrote this just for organization
class RendererMGLW(mglw.WindowConfig):
    gl_version = (3,3)
    title = "gpu 3d renderer"
    window_size = (800,600)
    resource_dir = '.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.core = RendererCore(self.ctx)

    def on_render(self, time, frame_time=0.0):
        aspect = self.wnd.aspect_ratio
        self.core.render(time, aspect)
