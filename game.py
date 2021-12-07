from OpenGL.GL import *
from OpenGL.GLUT import *
from numpy import array
from physics import Physics


class Game:
    window_width, window_height = 640, 480
    bufferId = 0

    physics_instance = Physics()

    @staticmethod
    def square_from_buffer():
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, Game.bufferId)
        glVertexPointer(2, GL_FLOAT, 0, None)
        glColor4f(1.0, 0.0, 0.0, 1.0)
        glDrawArrays(GL_QUADS, 0, 4)

    @staticmethod
    def square():
        glBegin(GL_QUADS)
        glVertex2f(100, 100)
        glVertex2f(200, 100)
        glVertex2f(200, 200)
        glVertex2f(100, 200)
        glEnd()

    @staticmethod
    def iterate():
        glViewport(0, 0, Game.window_width, Game.window_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-10, 10, -10, 10, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        pos = Game.physics_instance.body.position
        glTranslate(pos.x, pos.y, 0.0)

        error_code = glGetError()
        if error_code != 0:
            print(error_code)

    @staticmethod
    def show_screen():
        glClearColor(0.0, 1.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        Game.iterate()
        glColor3f(1.0, 0.0, 3.0)
        Game.square_from_buffer()
        glutSwapBuffers()

    @staticmethod
    def init_app():
        Game.bufferId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, Game.bufferId)
        vertices = array([-1, -1, 1, -1, 1, 1, -1, 1], dtype='float32')
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        glCullFace(GL_FRONT_AND_BACK)

    @staticmethod
    def mouse_func(button, state, x, y):
        pass

    @staticmethod
    def reshape(width, height):
        Game.window_width = width
        Game.window_height = height

    @staticmethod
    def main():
        Game.init_glut()
        Game.init_app()
        Game.game_timer(0)
        glutMainLoop()

    @staticmethod
    def game_timer(v):
        fps = 60
        msecs = round(1000 / fps)
        glutPostRedisplay()
        Game.physics_instance.run(msecs / 1000)
        glutTimerFunc(msecs, Game.game_timer, 5)

    @staticmethod
    def init_glut():
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(Game.window_width, Game.window_height)
        glutInitWindowPosition(100, 100)
        wind = glutCreateWindow("OpenGL Coding Practice")
        glutDisplayFunc(Game.show_screen)
        glutMouseFunc(Game.mouse_func)
        glutReshapeFunc(Game.reshape)
