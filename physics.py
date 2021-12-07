import pymunk  # Import pymunk..


class Physics:

    def __init__(self):
        self.space = pymunk.Space()  # Create a Space which contain the simulation
        self.space.gravity = 0, -981  # Set its gravity

        # ground
        ground = pymunk.Segment(self.space.static_body, a=(-100, -5), b=(100, -5), radius=1.0)
        ground.friction = 1.0
        self.space.add(ground)

    def run(self, step_size):
        self.space.step(step_size)  # Step the simulation one step forward
