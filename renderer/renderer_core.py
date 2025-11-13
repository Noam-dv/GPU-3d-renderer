import numpy as np
import moderngl
from rotation import RotationHandler
from render_util import *
from camera import Camera

from scenes.scene import Scene#scene types
from scenes.stest import STest

class RendererCore:
    #windowconfig is removed so pygame can use this renderrer too 
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx

        self.rot = RotationHandler()
        self.camera = Camera(eye=(0,2,5),target=(0,0,0),up=(0,1,0))

        self.scene = STest(self.ctx, self.camera, self.rot)#holds the current scene loaded 
        #stole this idea from unity and other game engines
        self.objects = []#list of objects
        #basically the way it works is scene will define a list of objects and ill keep a list of pointers to 
        #ever object
        #so if u move it and shit itll still render correctly
        self.load_scene(self.scene)

    def load_scene(self, scene: Scene):
        #store scene and grab its objects
        self.scene = scene
        self.scene.load()
        self.objects = self.scene.get_objects()

    def test_orbit(self, time, r=5.0, s=0.3, y=2.0):
        x=np.sin(time * s) * r 
        z=np.cos(time * s) * r
        self.camera.set_position((x, y, z))

    def render(self, time, aspect):
        self.ctx.clear(0., 0., 0., 1.0)

        #test cam movement
        self.test_orbit(time)

        for i in range(len(self.objects)):
            self.objects[i].render(time, aspect)
