import math
import sys
import random
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import argparse


def startup():
    update_viewport(None, 400, 400)
    glClearColor(1.0, 1.0, 1.0, 1.0)


def shutdown():
    pass

# Left vertex
def draw_triangle(x, y, a, inverted):
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)    # L
    glVertex2f(x+a, y)  # R
    h = a*math.sqrt(3)/2
    if inverted:    # MIDDLE
        h*=-1
    glVertex2f(x + a/2, y+h)
    glEnd()

def draw_fractal(x, y, a, depth):
    if depth == 0:
        return

    tr_w = a/2    # width of smaller triangle
    tr_h = tr_w*math.sqrt(3)/2  # height of smaller triangle
    tr_y = y + tr_h

    glColor3ub(255, 255, 255)
    draw_triangle(x+tr_w/2, tr_y, tr_w, True)
    for i in range(3):  # order: LB, TOP, RB
        if i%2 == 0:
            draw_fractal(x + i * tr_w / 2, y, tr_w, depth - 1)
        else:
            draw_fractal(x + i * tr_w / 2, y+tr_h, tr_w, depth - 1)

def draw_fractal_points(x, y, a, iterations=1000):
    h=a*math.sqrt(3)/2
    #Step 1: Pick 3 points of triangle
    leftP = (x, y)
    middleP = (x+a, y)
    rightP = (x+a/2, y+h)
    #Step 2: Seed -> middle points
    p = (x+a/2, y+h/3)
    glBegin(GL_POINTS)
    for i in range(iterations):
        #Step 3: Random vertex
        vertex = random.choice([leftP, middleP, rightP])
        #Step 4: Half point between vertex and p
        p = ((p[0]+vertex[0])/2, (p[1]+vertex[1])/2)
        #Step 5: Draw points
        glVertex2f(p[0], p[1])
    glEnd()



def render(time, version, colour):
    x = y = -100    # triangle origin (left vertex)
    a = 200         # triangle size
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(colour[0], colour[1], colour[2])  # random colour
    if version == 1:    # 1 wersja z tresci zadania
        draw_triangle(x, y, a, False)       # main triangle
        draw_fractal(x, y, a, 7)
    elif version == 2:  # 2 wersja z tresci zadania
        draw_fractal_points(x, y, a, 50000)
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
    frac_version = int(input("Fractal algorithm version (1 or 2): "))
    # parser = argparse.ArgumentParser()
    # parser.add_argument("frac_version", type=int)
    # args = parser.parse_args()
    if frac_version > 2 or frac_version < 1:
        print("Choose version between 1 and 2")
        sys.exit(-1)

    colour = []
    for i in range(3):
        colour.append(random.random())

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
        render(glfwGetTime(), frac_version, colour)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()