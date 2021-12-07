from OpenGL.GL import *
from OpenGL.GLUT import *
from numpy import array

from game import Game
from physics import Physics


if __name__ == "__main__":
    game = Game()
    game.main()
