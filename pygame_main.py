import pygame
import moderngl
import numpy as np
from renderer.renderer_core import RendererCore  # now importing from folder

#basically we will be using the scene already on the renderer class and display it on a pg window
def render():
    pygame.init()#setup pygame opengl
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("gpu 3d renderer (pygame window)")

    ctx = moderngl.create_context()

    #init the renderer with a existing contecxt s0 we can display it on the pg window
    renderer = RendererCore(ctx)

    clock = pygame.time.Clock()
    running = True
    start_time = pygame.time.get_ticks() / 1000.0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        t = pygame.time.get_ticks() / 1000.0
        frame_time = clock.get_time() / 1000.0

        #render! this is litterally all it takes due to the new renderer core and mglw classes
        renderer.render(t, 800/600)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    render()
