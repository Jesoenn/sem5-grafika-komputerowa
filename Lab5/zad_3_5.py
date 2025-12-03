#!/usr/bin/env python3
import sys
from enum import Enum

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

class LightComponent(Enum):
    AMBIENT = 0
    DIFFUSE = 1
    SPECULAR = 2

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

#Kolor materialu
mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0    # polyskliwosc

# Swiatla
light_ambient = [[0.1, 0.1, 0.0, 1.0], [0.1, 0.1, 0.0, 1.0]]
light_diffuse = [[0.8, 0.8, 0.0, 1.0], [1.0, 0.0, 1.0, 1.0]]
light_specular = [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]
light_position = [[0.0, 0.0, 10.0, 1.0], [5.0, 10.0, 0.0, 1.0]]

# Skladowe funkcji strat natezenia
att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

# Zmiana skladowych swiatla
key_pressed = False
change_index = 0
component = LightComponent.AMBIENT
increase = True
increase_val = 0.1


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # Swiatlo 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient[0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse[0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular[0])
    glLightfv(GL_LIGHT0, GL_POSITION, light_position[0])

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    # Swiatlo 1
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient[1])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse[1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular[1])
    glLightfv(GL_LIGHT1, GL_POSITION, light_position[1])

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

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

def check_value(min, value, max):
    if value > max:
        return max
    elif value < min:
        return min
    else:
        return value

# Zmiana swiatla nr 1
def change_light():
    global key_pressed, component, increase, increase_val, change_index
    global light_ambient, light_diffuse, light_specular, light_position

    change_mod = 1 if increase else -1
    if key_pressed:
        new_val = -1
        match component:
            case LightComponent.AMBIENT:
                new_val = check_value(0.0, light_ambient[1][change_index] + change_mod*increase_val, 1.0)
                light_ambient[1][change_index] = new_val
                glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient[1])
            case LightComponent.DIFFUSE:
                new_val = check_value(0.0, light_diffuse[1][change_index] + change_mod * increase_val, 1.0)
                light_diffuse[1][change_index] = new_val
                glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse[1])
            case LightComponent.SPECULAR:
                new_val = check_value(0.0, light_specular[1][change_index] + change_mod * increase_val, 1.0)
                light_specular[1][change_index] = new_val
                glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular[1])
        if new_val != -1:
            print(f"Nowa wartosc: {round(new_val, 1)}")
        key_pressed = False


def keyboard_key_callback(window, key, scancode, action, mods):
    global component, key_pressed, increase, change_index
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_UP and action == GLFW_PRESS:
        increase = True
        key_pressed = True
    elif key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        increase = False
        key_pressed = True
    elif key == GLFW_KEY_0 and action == GLFW_PRESS:
        change_index=0
    elif key == GLFW_KEY_1 and action == GLFW_PRESS:
        change_index=1
    elif key == GLFW_KEY_2 and action == GLFW_PRESS:
        change_index=2
    # Komponent
    elif key == GLFW_KEY_Q and action == GLFW_PRESS:
        component = LightComponent.AMBIENT
    elif key == GLFW_KEY_W and action == GLFW_PRESS:
        component = LightComponent.DIFFUSE
    elif key == GLFW_KEY_E and action == GLFW_PRESS:
        component = LightComponent.SPECULAR

    if action == GLFW_PRESS:
        print(f"Modyfikowanie komponentu {component}. Czy rosnaco: {increase}. Index: {change_index}")


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


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
        change_light()
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
