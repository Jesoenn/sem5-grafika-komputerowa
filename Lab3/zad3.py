import sys, math
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
import random

N = 25
tab = numpy.zeros((N,N,3))

def calc_xyz(u_arr, v_arr):
    for i, u in enumerate(u_arr):   # indeks, wartość
        for j, v in enumerate(v_arr):
            tab[i,j,0] = (-90*pow(u,5)+225*pow(u,4)-270*pow(u,3)+180*pow(u,2)-45*u)*math.cos(math.pi*v) # x
            tab[i,j,1] = 160 * pow(u, 4) - 320 * pow(u, 3) + 160 * pow(u, 2)-5  # y
            tab[i,j,2] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * math.sin(math.pi * v)   # z


u = numpy.linspace(0, 1, N)
v = numpy.linspace(0, 1, N)
calc_xyz(u, v)

def generate_egg_colours():
    egg_colour_arr = numpy.zeros((N, N, 3))
    for i in range(N):
        for j in range(N):
            egg_colour_arr[i,j] = [random.random(), random.random(), random.random()]
    return egg_colour_arr

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    # oś x
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    # oś y
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    # oś z
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def renderEgg(egg_vertices_colours):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(N-1):
        for j in range(N-1):
            # Pierwszy trojkat
            glColor3f(*egg_vertices_colours[i, j])
            glVertex3f(*tab[i, j])
            glColor3f(*egg_vertices_colours[i + 1, j])
            glVertex3f(*tab[i + 1, j])
            glColor3f(*egg_vertices_colours[i, j + 1])
            glVertex3f(*tab[i, j + 1])

            # Drugi trojkat (dopelniajacy)
            glVertex3f(*tab[i, j + 1])
            glColor3f(*egg_vertices_colours[i + 1, j])
            glVertex3f(*tab[i + 1, j])
            glColor3f(*egg_vertices_colours[i + 1, j + 1])
            glVertex3f(*tab[i + 1, j + 1])
    glEnd()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def render(time, egg_vertices_colours):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time*180/3.1415)
    axes()
    renderEgg(egg_vertices_colours)

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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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

    egg_vertices_colours = generate_egg_colours()   # Wygenerowanie kolorow
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), egg_vertices_colours)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
