from OpenGL.GL import *
from OpenGL.GLUT import *
from numpy import array

window_width, window_height = 500, 500
bufferId = 0


def square_from_buffer():
    glEnableClientState(GL_VERTEX_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, bufferId)
    glVertexPointer(2, GL_FLOAT, 0, None)
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glDrawArrays(GL_QUADS, 0, 4)


def square():
    glBegin(GL_QUADS)
    glVertex2f(100, 100)
    glVertex2f(200, 100)
    glVertex2f(200, 200)
    glVertex2f(100, 200)
    glEnd()


def iterate():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    errorCode = glGetError()
    if errorCode != 0:
        print(errorCode)


def show_screen():
    glClearColor(0.0, 1.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 0.0, 3.0)
    square_from_buffer()
    glutSwapBuffers()


def init_app():
    global bufferId
    bufferId = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, bufferId)
    vertices = array([-1, -1, 1, -1, 1, 1, -1, 1], dtype='float32')
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
    glCullFace(GL_FRONT_AND_BACK)


def mouse_func(button, state, x, y):
    pass


def timer(v):
    glutPostRedisplay()
    glutTimerFunc(1000 / 60, timer, v)


def reshape(width, height):
    global window_width
    global window_height
    window_width = width
    window_height = height


def init_glut():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    wind = glutCreateWindow("OpenGL Coding Practice")
    glutDisplayFunc(show_screen)
    glutMouseFunc(mouse_func)
    glutTimerFunc(100, timer, 0)
    glutReshapeFunc(reshape)


def main():
    init_glut()
    init_app()
    glutMainLoop()


if __name__ == "__main__":
    main()
