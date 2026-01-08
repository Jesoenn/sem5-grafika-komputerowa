#!/usr/bin/env python3
import math
import sys

import numpy
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image       # pillow


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

#Wektory normalne
egg_normal = numpy.zeros((N,N,3))
view_vectors = False

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
right_mouse_button_pressed = 0
mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.1, 1.0]
light_diffuse = [1.0, 1.0, 1.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

textures = []

def render_triangle(i:int, j:int, inverted=False):
    if not inverted:
        glTexCoord2f(u[i]*2, v[j])
    else:
        glTexCoord2f(2.0-u[i]*2, 1.0-v[j])
    glNormal(*egg_normal[i, j])
    glVertex3f(*tab[i, j])

def renderEgg():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(int((N-1)/2)):
        for j in range(N-1):
            # Pierwszy trojkat
            render_triangle(i, j)
            render_triangle(i+1, j)
            render_triangle(i, j+1)

            render_triangle(i, j+1)
            render_triangle(i+1, j)
            render_triangle(i+1, j + 1)
    glEnd()

    # Druga polowa trojkata odwrocona kolejnosc rysowania wierzcholkow
    glBegin(GL_TRIANGLES)
    for i in range(int((N-1)/2), N-1, 1):
        for j in range(N-1):
            render_triangle(i, j, True)
            render_triangle(i, j + 1, True)
            render_triangle(i + 1, j, True)

            render_triangle(i, j + 1, True)
            render_triangle(i + 1, j + 1, True)
            render_triangle(i + 1, j, True)
    glEnd()

def calc_egg_normal(u_arr, v_arr):
    global egg_normal
    tab_du = numpy.zeros((N, N, 3))
    tab_dv = numpy.zeros((N, N, 3))

    for i, u in enumerate(u_arr):   # indeks, wartość
        for j, v in enumerate(v_arr):
            tab_du[i,j,0] = (-450*pow(u,4)+900*pow(u,3)-810*pow(u,2)+360*u-45)*math.cos(math.pi*v) # x
            tab_du[i,j,1] = 640 * pow(u, 3) - 960 * pow(u, 2) + 320 * u  # y
            tab_du[i,j,2] = (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * math.sin(math.pi * v)   # z

            tab_dv[i, j, 0] = math.pi * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * math.sin(math.pi * v)  # x
            tab_dv[i, j, 1] = 0.0 # y
            tab_dv[i, j, 2] = -math.pi * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * math.cos(math.pi * v)  # z

    # Obliczenie wektorow normalnych
    for u in range(N):
        for v in range(N):
            egg_normal[u][v][0] = tab_du[u][v][1] * tab_dv[u][v][2] - tab_du[u][v][2] * tab_dv[u][v][1]
            egg_normal[u][v][1] = tab_du[u][v][2] * tab_dv[u][v][0] - tab_du[u][v][0] * tab_dv[u][v][2]
            egg_normal[u][v][2] = tab_du[u][v][0] * tab_dv[u][v][1] - tab_du[u][v][1] * tab_dv[u][v][0]

            # Normalizacja
            vector_length = numpy.linalg.norm(egg_normal[u][v])
            if vector_length == 0:
                vector_length = 1
            for i in range(3):
                egg_normal[u][v][i] = egg_normal[u][v][i]/vector_length

    # Odwrocenie od polowy jajka
    for i in range(int(N/2), N-1, 1):
        for j in range(N):
            egg_normal[i][j][0] *= -1
            egg_normal[i][j][1] *= -1
            egg_normal[i][j][2] *= -1

    for v in range(N):
        egg_normal[int(N/2)][v][0] = 0.0
        egg_normal[int(N/2)][v][1] = 1.0
        egg_normal[int(N/2)][v][2] = 0.0

        egg_normal[0][v][0] = 0.0
        egg_normal[0][v][1] = -1.0
        egg_normal[0][v][2] = 0.0
        egg_normal[N-1][v][0] = 0.0
        egg_normal[N-1][v][1] = -1.0
        egg_normal[N-1][v][2] = 0.0

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Odczyt tekstur do pamieci
    file_names = ["tekstura.tga", "tekstura_moja.tga"]
    for i in range(len(file_names)):
        textures.append(Image.open(file_names[i]))

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, textures[0].size[0], textures[0].size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, textures[0].tobytes("raw", "RGB", 0, -1)
    )


def shutdown():
    pass

def change_texture(texture_num : int):
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, textures[texture_num].size[0], textures[texture_num].size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, textures[texture_num].tobytes("raw", "RGB", 0, -1)
    )

def render(time):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    calc_egg_normal(u, v)
    renderEgg()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global render_wall, texture_num
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_1 and action == GLFW_PRESS:
        change_texture(0)
    elif key == GLFW_KEY_2 and action == GLFW_PRESS:
        change_texture(1)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
