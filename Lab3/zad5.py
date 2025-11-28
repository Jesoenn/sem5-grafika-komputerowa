import sys, math
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

pyramids = []   # Wszystkie piramidy
colours = []    # Wszystkie kolory


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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time*180/3.1415/2)
    axes()
    render_pyramids()

    glFlush()

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
                150.0, -150.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                150.0, -150.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



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
    glfwSwapInterval(1)

    set_up()    # ustawienie wierzchołków głównego trójkąta
    calculate_triangles(triangle_iterations)    # wykonanie iteracji algorytmu
    colours = calculate_colours()  # interpolacja kolorow na podstawie duzego trojkata

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
