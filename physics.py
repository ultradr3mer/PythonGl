import pymunk  # Import pymunk..


class Physics:

    def __init__(self):
        self.space = pymunk.Space()  # Create a Space which contain the simulation
        self.space.gravity = 0, -98.1  # Set its gravity

        # ground
        ground = pymunk.Segment(self.space.static_body, a=(-10, -10), b=(10, -10), radius=1.0)
        ground.friction = 0.7
        self.space.add(ground)

    def run(self, step_size):
        self.space.step(step_size)  # Step the simulation one step forward
