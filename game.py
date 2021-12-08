from OpenGL.GL import *
from OpenGL.GLUT import *

from box import Box
from physics import Physics
from drawable import Drawable
from game_math import Rectangle


class Game:
    window_width, window_height = 640, 480
    fps = 60
    physics_instance: Physics = None
    drawables: list[Drawable] = list()
    viewable_area = Rectangle(0, 0, 0, 0)

    @staticmethod
    def draw_frame():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, Game.window_width, Game.window_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect = Game.window_width / Game.window_height
        area = Rectangle(-10 * aspect, 10 * aspect, -10, 10)
        glOrtho(area.left, area.right, area.bottom, area.top, 0.0, 1.0)
        Game.viewable_area = area

        for d in Game.drawables:
            d.draw()

        error_code = glGetError()
        if error_code != 0:
            print(error_code)

        glutSwapBuffers()

    @staticmethod
    def init_app():
        Drawable.init()
        Box.init()
        Game.physics_instance = Physics()
        Game.drawables.append(Box())

        floor = Drawable()
        floor.position = (0, -11)
        floor.size = (7, 2)
        Game.drawables.append(floor)

    @staticmethod
    def mouse_func(button, state, x, y):
        if button == 0 and state == 0:
            screen_area = Rectangle(0, Game.window_width, Game.window_height, 0)
            pos = Game.viewable_area.project(screen_area, (x, y))
            new_box = Box()
            new_box.position = pos
            Game.drawables.append(new_box)

    @staticmethod
    def reshape(width, height):
        Game.window_width = width
        Game.window_height = height

    @staticmethod
    def main():
        Game.init_glut()
        Game.init_app()
        Game.game_timer()
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
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glMinSampleShading(4)
        glClearColor(0.0, 0.0, 0.0, 0.0)
