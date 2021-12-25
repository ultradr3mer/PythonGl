import math
import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from drawable_text import DrawableText
from mesh import Mesh
from physics import Physics
from drawable import Drawable
from game_math import Rectangle
from glm import orthoLH_ZO

from punisher import Punisher
from shader import Shader
from tex import Tex


class PillTemplate:
    def __init__(self, mesh, tex, ghost, size):
        self.mesh = mesh
        self.tex = tex
        self.ghost = ghost
        self.size = size

        self.ghost.size = (size, size)


class Game:
    default_shader = None
    window_width, window_height = 640, 480
    fps = 60
    physics_instance: Physics = None
    drawables: list[Drawable] = list()
    templates: list[PillTemplate] = list()
    updatebles = list()
    viewable_area = Rectangle(0, 0, 0, 0)
    current_template: PillTemplate = None

    q_pressed = False
    e_pressed = False

    size = 0.7

    score_counter = 0

    score_text: DrawableText = None

    @staticmethod
    def draw_frame():
        glViewport(0, 0, Game.window_width, Game.window_height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        aspect = Game.window_width / Game.window_height
        area = Rectangle(-10 * aspect, 10 * aspect, -10, 10)
        Game.projection_matrix = orthoLH_ZO(area.left, area.right, area.bottom, area.top, 0.0, 1.0)
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
        instance = Game.physics_instance
        if button == 0 and state == 0:
            pos = Game.world_pos_from_screen(x, y)
            body = instance.find_object(pos)
            if body:
                instance.start_grab(body, pos)
                return
            pill = Game.create_new_pill()
            pill.position = pos
            Game.drawables.append(pill)
            return
        elif button == 0 and state == 1:
            instance.end_grab()

    @staticmethod
    def passive_motion(x, y):
        Game.current_template.ghost.position = Game.world_pos_from_screen(x, y)

    @staticmethod
    def motion_func(x, y):
        instance = Game.physics_instance
        pos = Game.world_pos_from_screen(x, y)
        instance.update_grab(pos)

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

        rotation_speed = 0.04
        if Game.q_pressed:
            Game.current_template.ghost.angle += rotation_speed
        if Game.e_pressed:
            Game.current_template.ghost.angle -= rotation_speed

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
        glutMotionFunc(Game.motion_func)
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
        default_shader = Shader("assets/shader.vs.c", "assets/shader.fs.c")
        font_shader = Shader("assets/font_shader.vs.c", "assets/font_shader.fs.c")
        numbers = Tex("assets/numbers.dds")

        floor = Drawable(box_mesh, default_shader)
        floor.add_tex(floor_tex)
        floor.position = (0.0, -11.0)
        floor.size = (10, 2)
        Game.drawables.append(floor)

        punisher_mesh = Mesh("assets/punisher.obj")
        punisher_tex = Tex("assets/punisher_texture.dds")
        punisher_ghost_tex = Tex("assets/punisher_glow.dds")
        punisher_ghost = Drawable(punisher_mesh, default_shader)
        punisher_ghost.visible = False
        punisher_ghost.size = (Game.size, Game.size)
        punisher_ghost.add_tex(punisher_ghost_tex)
        Game.drawables.append(punisher_ghost)
        Game.templates.append(PillTemplate(punisher_mesh, punisher_tex, punisher_ghost, 0.75))

        plein_mesh = Mesh("assets/philipp_plein.obj")
        plein_tex = Tex("assets/philipp_plein.dds")
        plein_ghost_tex = Tex("assets/philipp_plein_glow.dds")
        plein_ghost = Drawable(plein_mesh, default_shader)
        plein_ghost.visible = False
        plein_ghost.size = (Game.size, Game.size)
        plein_ghost.add_tex(plein_ghost_tex)
        Game.drawables.append(plein_ghost)
        Game.templates.append(PillTemplate(plein_mesh, plein_tex, plein_ghost, 0.6))

        mesh = Mesh("assets/tesla.obj")
        tex = Tex("assets/tesla.dds")
        ghost_tex = Tex("assets/tesla_ghost.dds")
        ghost = Drawable(mesh, default_shader)
        ghost.visible = False
        ghost.size = (Game.size, Game.size)
        ghost.add_tex(ghost_tex)
        Game.drawables.append(ghost)
        Game.templates.append(PillTemplate(mesh, tex, ghost, 0.6))

        score_text = DrawableText(font_shader, "Anzahl")
        score_text.position = (-9, 8)
        score_text.size = (1, 1)
        score_text.add_tex(numbers)
        score_text.color = (0.3, 0.7, 1.0, 1.0)
        Game.drawables.append(score_text)
        Game.score_text = score_text

        Game.default_shader = default_shader
        Game.physics_instance = Physics()
        Game.randomize_next_pill()
        Game.create_new_pill()

    @staticmethod
    def create_new_pill():
        template = Game.current_template
        pill = Punisher(template.mesh, Game.default_shader, template.size)
        pill.add_tex(template.tex)
        pill.angle = template.ghost.angle
        Game.drawables.append(pill)
        Game.updatebles.append(pill)
        Game.score_counter += 1
        Game.update_score()
        Game.randomize_next_pill()
        return pill

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

    @staticmethod
    def update_score():
        Game.score_text.set_text(f"Anzahl: {Game.score_counter}")

    @staticmethod
    def randomize_next_pill():
        template = Game.current_template
        if template:
            Game.current_template.ghost.visible = False
            angle = template.ghost.angle
        else:
            angle = random.randrange(0, 100) / 100 * math.pi * 2.0
        template = Game.templates[random.randrange(0, len(Game.templates))]
        template.ghost.visible = True
        template.ghost.angle = angle
        Game.current_template = template
        pass
