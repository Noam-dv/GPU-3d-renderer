import moderngl_window as mglw
from renderer.renderer_mglw import RendererMGLW
import pygame

if __name__ == "__main__":
    pygame.init()
    mglw.run_window_config(RendererMGLW)#this just runs the window on the modergl renderer