class Rectangle:
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

    def project(self, origin_space: 'Rectangle', point):
        x, y = point

        normalized_x = (x - origin_space.left) / (origin_space.right - origin_space.left)
        normalized_y = (y - origin_space.top) / (origin_space.bottom - origin_space.top)

        result_x = normalized_x * (self.right - self.left) + self.left
        result_y = normalized_y * (self.bottom - self.top) + self.top

        return result_x, result_y
