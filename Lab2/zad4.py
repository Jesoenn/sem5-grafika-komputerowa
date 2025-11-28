import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import argparse


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0, 0, 0, 1.0)


def shutdown():
    pass

# lewy dolny rog
def draw_rectangle(x, y, a, b):
    # lewy trojkat
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x+a, y)
    glVertex2f(x, y+b)
    glEnd()

    # prawy trojkat
    glBegin(GL_TRIANGLES)
    glVertex2f(x+a, y+b)
    glVertex2f(x+a, y)
    glVertex2f(x, y+b)
    glEnd()

def draw_fractal(x, y, a, b, depth):
    if depth == 0:
        return
    glColor3ub(255, 255, 255)

    rect_w = a/3    # width of smaller rectangle
    rect_h = b/3    # height of smaller rectangle

    for row in range(3):
        for col in range(3):
            if col == 1 and row == 1:   # draw in the middle of big rectangle
                draw_rectangle(x+rect_w, y+rect_h, rect_w, rect_h)
            else:   # keep "dividing" into smaller rectangles
                draw_fractal(x + rect_w * col, y + rect_h * row, rect_w, rect_h, depth - 1)



def render(time, depth):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3ub(0, 0, 0)
    draw_fractal(-100,-100,200,200, depth)

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
    depth = int(input("Fractal depth: "))
    # parser = argparse.ArgumentParser()
    # parser.add_argument("depth", type=int)
    # args = parser.parse_args()

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
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), depth)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
