from OpenGL.GL import *
from OpenGL.GLUT import *
from numpy import array

w, h = 500, 500
bufferId = 0


# ---Section 1---
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


# Add this function before Section 2 of the code above i.e. the showScreen function
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    errorCode = glGetError()
    if errorCode != 0:
        print(errorCode)


# ---Section 2---

def show_screen():
    glClearColor(0.0, 1.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Remove everything from screen (i.e. displays all white)
    glLoadIdentity()  # Reset all graphic/shape's position
    iterate()
    glColor3f(1.0, 0.0, 3.0)  # Set the color to pink
    square_from_buffer()  # Draw a square using our function
    glutSwapBuffers()


def init_app():
    global bufferId
    bufferId = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, bufferId)
    vertices = array([-1, -1, 1, -1, 1, 1, -1, 1], dtype='float32')
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
    glCullFace(GL_FRONT_AND_BACK)


# ---Section 3---

glutInit()
glutInitDisplayMode(GLUT_RGBA)  # Set the display mode to be colored
glutInitWindowSize(500, 500)  # Set the w and h of your window
glutInitWindowPosition(0, 0)  # Set the position at which this windows should appear
wind = glutCreateWindow("OpenGL Coding Practice")  # Set a window title
glutDisplayFunc(show_screen)
glutIdleFunc(show_screen)  # Keeps the window open
init_app()
glutMainLoop()  # Keeps the above created window displaying/running in a loop
