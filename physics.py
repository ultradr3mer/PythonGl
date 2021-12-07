import pymunk  # Import pymunk..


class Physics:

    def __init__(self):
        self.space = pymunk.Space()  # Create a Space which contain the simulation
        self.space.gravity = 0, -981  # Set its gravity

        self.body = pymunk.Body()  # Create a Body
        self.body.position = 0, 0  # Set the position of the body

        self.poly = pymunk.Poly.create_box(self.body, size=(2, 2))  # Create a box shape and attach to body
        self.poly.mass = 10  # Set the mass on the shape
        self.space.add(self.body, self.poly)  # Add both body and shape to the simulation

        # ground
        ground = pymunk.Segment(self.space.static_body, a=(-100, -5), b=(100, -5), radius=1.0)
        ground.friction = 1.0
        self.space.add(ground)

    def run(self, step_size):
        self.space.step(step_size)  # Step the simulation one step forward
