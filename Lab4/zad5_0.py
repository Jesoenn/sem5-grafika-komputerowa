import sys, math

import numpy
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


pyramids = []   # Wszystkie piramidy
colours = []    # Wszystkie kolory

pix2angle = 1.0

# Mouse movement
sensitivity = 0.5
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

# Wspolrzedne
movement_sideways = 0
movement_forward = 0
movement_speed = 2.0
viewer = [200.0, 0.0, 0.0]
camera_up = [0.0, 1.0, 0.0]
camera_front = [1.0, 0.0, 0.0]
theta = 0.0 # obrot prawo/lewo
phi = 0.0   # obrot gora/dol


def calculate_colours():
    c_pyramids = [] # kolory dla piramid
    for pyramid in pyramids:
        c_vertices = []
        for v in pyramid:
            c_rgb = [(abs(v[0]+75.0))/150.0,  abs(v[1]+100)/150.0, 1-(abs(v[2]+75.0))/150.0]
            c_vertices.append(c_rgb)
        c_pyramids.append(c_vertices)

    return c_pyramids


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
    glVertex3f(-50.0, 0.0, 0.0)
    glVertex3f(50.0, 0.0, 0.0)

    # oś y
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -50.0, 0.0)
    glVertex3f(0.0, 50.0, 0.0)

    # oś z
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -50.0)
    glVertex3f(0.0, 0.0, 50.0)

    glEnd()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    global viewer, yaw, pitch, camera_front, camera_up
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              viewer[0]+camera_front[0], viewer[1]+camera_front[1], viewer[2]+camera_front[2],
              camera_up[0], camera_up[1], camera_up[2])

    axes()
    render_pyramids()



    glFlush()

def move():
    global movement_sideways, movement_forward, movement_speed, camera_front, camera_up, viewer

    viewer[0] += camera_front[0] * movement_speed * movement_forward
    viewer[1] += camera_front[1] * movement_speed * movement_forward
    viewer[2] += camera_front[2] * movement_speed * movement_forward

    perpendicular_vector = numpy.cross(camera_front, camera_up)


    viewer[0] -= perpendicular_vector[0] * movement_speed * movement_sideways
    viewer[1] -= perpendicular_vector[1] * movement_speed * movement_sideways
    viewer[2] -= perpendicular_vector[2] * movement_speed * movement_sideways

def move_camera():
    global camera_front, theta, phi, delta_x, delta_y

    theta += delta_x*pix2angle*sensitivity
    phi += delta_y*pix2angle*sensitivity

    theta %= 360
    # Patrzenie max 90 stopni do góry i na dol
    if phi > 89:
        phi = 89
    elif phi < -89:
        phi = -89

    x = math.cos(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    y = math.sin(-phi * math.pi / 180)  # -phi zeby ruch myszka w dol to patrzenie w dol
    z = math.sin(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    camera_front = [x, y, z]
    delta_x = 0
    delta_y = 0


def render_pyramids():
    glBegin(GL_TRIANGLES)
    # pyramids[0] -> lista wierzcholkow piramidy
    # pyramids[0][0-3] -> wierzchołek 1,2,3,góra
    # pyramids[0][0][0-2] -> x -> y -> z

    for p, pyramid in enumerate(pyramids):
        # Podstawa 1
        glColor3f(*colours[p][0])
        glVertex3f(*pyramid[0])
        glColor3f(*colours[p][1])
        glVertex3f(*pyramid[1])
        glColor3f(*colours[p][2])
        glVertex3f(*pyramid[2])

        # Ściany
        for i in range(3):
            glColor3f(*colours[p][i])
            glVertex3f(*pyramid[i])
            glColor3f(*colours[p][(i+1)%3])
            glVertex3f(*pyramid[(i+1)%3])   # dla i=2, i+1=3 (czyli 0)
            glColor3f(*colours[p][3])
            glVertex3f(*pyramid[3])
    glEnd()


def calculate_triangles(triangle_iterations):
    global pyramids
    # pyramids[0] -> lista wierzcholkow piramidy
    # pyramids[0][0-3] -> wierzchołek 0,1,2,góra
    # pyramids[0][0][0-2] -> x -> y -> z

    for i in range(triangle_iterations):  # liczba iteracji fraktala
        new_pyramids = []
        for pyramid in pyramids:  # dla każdej piramidy
            for vertex in pyramid:  # dla kazdego wierzcholka
                small_pyramid = []
                # Zmniejszenie dlugosci boku o polowe przesuwajac 'v' w strone wierzcholka vertex
                for v in pyramid:
                    v_new = [(vertex[0]+v[0])/2, (vertex[1]+v[1])/2, (vertex[2]+v[2])/2]
                    small_pyramid.append(v_new)
                new_pyramids.append(small_pyramid)
        pyramids = new_pyramids


def set_up():
    a = 150.0 # dlugosc boku trojkata glownego
    main_triangle = [
        [-a/2.0, -a*math.sqrt(6)/6.0, -a*math.sqrt(3)/4.0],  # v0 podstawy
        [a/2.0, -a*math.sqrt(6)/6.0, -a*math.sqrt(3)/4.0],  # v1 podstawy
        [0.0, -a*math.sqrt(6)/6.0, a*math.sqrt(3)/4.0],  # v2 podstawy
        [0.0, a*math.sqrt(6)/6.0, 0.0]  # v3 gora
    ]
    pyramids.append(main_triangle)

def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 3000.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard_key_callback(window, key, scancode, action, mods):
    global movement_sideways, movement_forward
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_W:
        if action == GLFW_PRESS:
            if movement_forward == -1:  # jezeli S jest nacisniete
                movement_forward = 0
            else:
                movement_forward = 1
        elif action == GLFW_RELEASE:
            if movement_forward == 1:
                movement_forward = 0
            elif movement_forward == 0:  # jezeli S jest nacisniete
                movement_forward = -1

    elif key == GLFW_KEY_S:
        if action == GLFW_PRESS:
            if movement_forward == 1:   # jezeli W jest nacisniete
                movement_forward = 0
            else:
                movement_forward = -1
        elif action == GLFW_RELEASE:
            if movement_forward == -1:
                movement_forward = 0
            elif movement_forward == 0:  # jezeli W jest nacisniete
                movement_forward = 1

    if key == GLFW_KEY_A:
        if action == GLFW_PRESS:
            if movement_sideways == -1:  # jezeli D jest nacisniete
                movement_sideways = 0
            else:
                movement_sideways = 1
        elif action == GLFW_RELEASE:
            if movement_sideways == 1:
                movement_sideways = 0
            elif movement_sideways== 0:  # jezeli D jest nacisniete
                movement_sideways = -1

    elif key == GLFW_KEY_D:
        if action == GLFW_PRESS:
            if movement_sideways == 1:  # jezeli A jest nacisniete
                movement_sideways = 0
            else:
                movement_sideways= -1
        elif action == GLFW_RELEASE:
            if movement_sideways== -1:
                movement_sideways = 0
            elif movement_sideways == 0:  # jezeli A jest nacisniete
                movement_sideways = 1

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, mouse_x_pos_old, delta_y, mouse_y_pos_old, yaw, pitch, sensitivity

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

def main():
    global colours
    triangle_iterations = int(input("Liczba iteracji algorytmu (>=0): "))
    if triangle_iterations < 0:
        triangle_iterations = 0

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
    glfwSwapInterval(1)

    set_up()    # ustawienie wierzchołków głównego trójkąta
    calculate_triangles(triangle_iterations)    # wykonanie iteracji algorytmu
    colours = calculate_colours()  # interpolacja kolorow na podstawie duzego trojkata

    startup()
    while not glfwWindowShouldClose(window):
        move()
        move_camera()
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
