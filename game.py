import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.raw.GLU import gluPerspective

from mesh import Mesh
from physics_body import PhysicsBody
from physics import Physics
from drawable import Drawable
from game_math import Rectangle
import glm

from shader import Shader
from tex import Tex


class Game:
    default_shader = None
    punisher_tex = None
    punisher_mesh = None
    window_width, window_height = 640, 480
    fps = 60
    physics_instance: Physics = None
    drawables: list[Drawable] = list()
    updatebles = list()
    viewable_area = Rectangle(0, 0, 0, 0)
    ghost: Drawable = None

    q_pressed = False
    e_pressed = False

    @staticmethod
    def draw_frame():
        glViewport(0, 0, Game.window_width, Game.window_height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        aspect = Game.window_width / Game.window_height
        area = Rectangle(-10 * aspect, 10 * aspect, -10, 10)
        Game.projection_matrix = glm.orthoLH_ZO(area.left, area.right, area.bottom, area.top, 0.0, 1.0)
        Game.viewable_area = area

        for d in Game.drawables:
            d.draw()

        error_code = glGetError()
        if error_code != 0:
            print(error_code)

        glFlush()
        glFinish()
        glutSwapBuffers()
        Game.read_error_log()

    @staticmethod
    def mouse_func(button, state, x, y):
        if button == 0 and state == 0:
            pun = Game.create_new_punisher()
            pun.body.position = Game.world_pos_from_screen(x, y)
            pun.body.angle = Game.ghost.angle
            Game.drawables.append(pun)

    @staticmethod
    def passive_motion(x, y):
        Game.ghost.position = Game.world_pos_from_screen(x, y)

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

        for u in Game.updatebles:
            u.update()

        glutTimerFunc(msecs, lambda v: Game.game_timer(), 5)

        rotation_speed = 0.02
        if Game.q_pressed:
            Game.ghost.angle += rotation_speed
        if Game.e_pressed:
            Game.ghost.angle -= rotation_speed

    @staticmethod
    def key_function(uchar, x, y):
        if uchar == b"q":
            Game.q_pressed = True
        if uchar == b"e":
            Game.e_pressed = True

    @staticmethod
    def key_up_function(uchar, x, y):
        if uchar == b"q":
            Game.q_pressed = False
        if uchar == b"e":
            Game.e_pressed = False

    @staticmethod
    def init_glut():
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
        glutInitWindowSize(Game.window_width, Game.window_height)
        glutInitWindowPosition(100, 100)

        glutCreateWindow("Python Gl sandbox")
        glutDisplayFunc(Game.draw_frame)
        glutMouseFunc(Game.mouse_func)
        glutReshapeFunc(Game.reshape)
        glutPassiveMotionFunc(Game.passive_motion)
        glutKeyboardUpFunc(Game.key_up_function)
        glutKeyboardFunc(Game.key_function)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(0.1, 0.1, 0.1, 0.0)
        glEnable(GL_DEBUG_OUTPUT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    @staticmethod
    def init_app():
        box_mesh = Mesh("assets/box.obj")
        floor_tex = Tex("assets/floor.dds")
        punisher_mesh = Mesh("assets/punisher.obj")
        punisher_tex = Tex("assets/punisher_texture.dds")
        ghost_tex = Tex("assets/punisher_glow.dds")
        default_shader = Shader("assets/shader.vs.c", "assets/shader.fs.c")

        floor = Drawable(box_mesh, default_shader)
        floor.add_tex(floor_tex)
        floor.position = (0.0, -11.0)
        floor.size = (10, 2)
        Game.drawables.append(floor)

        ghost = Drawable(punisher_mesh, default_shader)
        ghost.add_tex(ghost_tex)
        Game.drawables.append(ghost)
        Game.ghost = ghost

        Game.punisher_mesh = punisher_mesh
        Game.default_shader = default_shader
        Game.punisher_tex = punisher_tex
        Game.physics_instance = Physics()
        Game.create_new_punisher()

    @staticmethod
    def create_new_punisher():
        pun = PhysicsBody(Game.punisher_mesh, Game.default_shader)
        pun.add_tex(Game.punisher_tex)
        Game.drawables.append(pun)
        Game.updatebles.append(pun)
        return pun

    @staticmethod
    def read_error_log():
        while glGetIntegerv(GL_DEBUG_LOGGED_MESSAGES) > 0:
            length = glGetIntegerv(GL_MAX_DEBUG_MESSAGE_LENGTH)
            message_array = glGetDebugMessageLog(1, length)
            message = str(message_array[2].tostring().replace(b'\x00', b''))
            print(message)

    @staticmethod
    def world_pos_from_screen(x, y):
        screen_area = Rectangle(0, Game.window_width, Game.window_height, 0)
        return Game.viewable_area.project(screen_area, (x, y))
