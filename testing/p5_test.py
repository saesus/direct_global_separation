# Testing code for whether or not GLSL works with processing

from p5 import *


def setup():
    size(640, 360)
    background(204)


def draw():
    background(205, 102, 94)
    rotate_x(frame_count * 0.01)
    rotate_y(frame_count * 0.01)
    cone(40, 70)


# OpenGL works but needs pyopengl
# Also pip installing p5 isnt updated so it needs to be manually updated from github
# research into vispy maybe

run(mode="P3D")
