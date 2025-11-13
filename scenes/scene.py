import numpy as np
import moderngl
from renderer.rendered_object import RenderedObject
from render_util import *
from spacetime import RenderedSpacetime

class Scene:
    #scene has a list of objects
    #the scene also keeps shaders and shit and has a shared rot handler
    def __init__(self):
        self.objects = []  #list of renderable objects

    def get_objects(self):
        return self.objects

    def load(self):
        for i in self.objects:
            i.load()

    def render(self, time, aspect):
        for i in self.objects:
            i.render(time, aspect)