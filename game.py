from OpenGL.GL import *
from OpenGL.GLUT import *
from physics import Physics
from drawable import Drawable


class Game:
    window_width, window_height = 640, 480
    fps = 60

    physics_instance = Physics()

    box = None  # type: Drawable

    @staticmethod
    def draw_frame():
        glClearColor(0.0, 1.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, Game.window_width, Game.window_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect = Game.window_width / Game.window_height
        glOrtho(-10 * aspect, 10 * aspect, -10, 10, 0.0, 1.0)

        Game.box.draw()

        error_code = glGetError()
        if error_code != 0:
            print(error_code)

        glutSwapBuffers()

    @staticmethod
    def init_app():
        Drawable.init()

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
        Game.game_timer()
        Game.box = Drawable()
        glutMainLoop()

    @staticmethod
    def game_timer():
        msecs = round(1000.0 / Game.fps)
        glutPostRedisplay()
        Game.physics_instance.run(msecs / 1000.0)
        glutTimerFunc(msecs, lambda v: Game.game_timer(), 5)

    @staticmethod
    def init_glut():
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(Game.window_width, Game.window_height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow("OpenGL Coding Practice")
        glutDisplayFunc(Game.draw_frame)
        glutMouseFunc(Game.mouse_func)
        glutReshapeFunc(Game.reshape)
