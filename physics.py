import pymunk  # Import pymunk..
from pymunk import Vec2d

import game
import physics_body


class Physics:

    def __init__(self):
        self.space = pymunk.Space()  # Create a Space which contain the simulation
        self.space.gravity = 0, -98.1  # Set its gravity
        ground = pymunk.Segment(self.space.static_body, a=(-10, -10), b=(10, -10), radius=1.0)
        ground.friction = 0.7
        self.space.add(ground)
        self._grab_joint: pymunk.PivotJoint = None

    def run(self, step_size):
        self.space.step(step_size)  # Step the simulation one step forward

    def find_object(self, position) -> physics_body.PhysicsBody:
        for d in game.Game.drawables:
            if isinstance(d, physics_body.PhysicsBody):
                pqi = d.poly.point_query(position)
                if pqi.distance <= 0.0:
                    return d
        return None

    def start_grab(self, body: physics_body.PhysicsBody, pos):
        self._grab_joint = pymunk.PivotJoint(body.body, self.space.static_body, pos)
        self.space.add(self._grab_joint)
        pass

    def update_grab(self, pos):
        if not self._grab_joint:
            return
        self._grab_joint.anchor_b = pos

    def end_grab(self):
        if not self._grab_joint:
            return
        self.space.remove(self._grab_joint)
        self._grab_joint = None
        pass
