import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

# lewy dolny rog
def draw_rectangle(x, y, a, b, colour, d=0.0):
    glColor3f(colour[0], colour[1], colour[2])
    # lewy trojkat
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)    # LB
    glVertex2f(x+a+a*d, y)  # RB
    glVertex2f(x, y+b-b*d)  # LT
    glEnd()

    # prawy trojkat
    glBegin(GL_TRIANGLES)
    glVertex2f(x+a+a*d, y+b)    # RT
    glVertex2f(x+a+a*d, y)      # RB
    glVertex2f(x, y+b-b*d)      # LT
    glEnd()


def render(time, deformation, colour):
    glClear(GL_COLOR_BUFFER_BIT)
    draw_rectangle(-50.0, 20.0, 100.0, 50.0, colour)
    draw_rectangle(-50.0, -75.0, 100.0, 50.0, colour, deformation)

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()

    deformation = random.random()   # Zad 3 deformacja
    colour = []
    for i in range(3):
        colour.append(random.random())

    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), deformation, colour)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
