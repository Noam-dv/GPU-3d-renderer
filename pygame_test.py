import pygame
import moderngl
import numpy as np
from pygame.locals import DOUBLEBUF, OPENGL

#pygame init
pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

sc = pygame.display.set_mode((800, 600), DOUBLEBUF|OPENGL)
pygame.display.set_caption("pygame window with moderngl")

ctx = moderngl.create_context()

#basic shaders
prog = ctx.program(
    vertex_shader="""
        #version 330
        in vec2 in_vert;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
    """,
    fragment_shader="""
        #version 330
        out vec4 fragColor;
        void main() {
            fragColor = vec4(1.0, 0.75, 0.2, 1.0);
        }
    """
)

v = np.array([
    [-0.6, -0.6],
    [ 0.6, -0.6],
    [ 0.0,  0.6],
], dtype='f4')

#vertex buffer
vbuffer = ctx.buffer(v.tobytes())
varr = ctx.vertex_array(prog, [(vbuffer, '2f', 'in_vert')])

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.1, 0.1, 0.1)#gray bg for test
    varr.render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
