import game
from physics_body import PhysicsBody


class Punisher(PhysicsBody):
    def __init__(self, mesh, shader, scale):
        super().__init__(mesh, shader, scale)
        self.above = True
        pass

    def update(self):
        super().update()
        if self.position.y < -10 and self.above:
            game.Game.counter -= 1
            print(game.Game.counter)
            self.above = False

