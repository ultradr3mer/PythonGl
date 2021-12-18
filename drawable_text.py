from drawable import Drawable
from generated_mesh import GenMesh


class DrawableText(Drawable):
    base_verts = [[1.0, 0.0],
                  [0.0, 1.0],
                  [0.0, 0.0],
                  [1.0, 0.0],
                  [1.0, 1.0],
                  [0.0, 1.0]]

    base_tex_coords = [[0.9999, 0.9999],
                       [0.0001, 0.0001],
                       [0.0001, 0.9999],
                       [0.9999, 0.9999],
                       [0.9999, 0.0001],
                       [0.0001, 0.0001]]

    character_map = {
        '1': (0, 0),
        '2': (1, 0),
        '3': (2, 0),
        '4': (3, 0),
        '5': (4, 0),
        '6': (5, 0),
        '7': (6, 0),
        '8': (7, 0),
        '9': (8, 0),
        '0': (9, 0)
    }

    def __init__(self, shader, text=""):
        self.mesh = GenMesh()
        self.generate_mesh(text)
        super(DrawableText, self).__init__(self.mesh, shader)

    def generate_mesh(self, text):
        verts = list()
        tex_coords = list()

        x_pos = 0
        for current_character in text:
            verts.extend(self.transform_vec3(self.base_verts, pos=(x_pos, 0), size=(24.0 / 32.0, 1.0)))
            tex_coords.extend(self.transform_vec2(self.base_tex_coords,
                                                  size=(24.0 / 256.0, 32.0 / 256.0),
                                                  pos=self.character_map[current_character]))
            x_pos += 1

        self.mesh.update(verts, tex_coords)

    @staticmethod
    def transform_vec3(points, pos, size):
        result = list()
        for v in points:
            result.append(((v[0] + pos[0]) * size[0],
                           (v[1] + pos[1]) * size[1],
                           0.0))

        return result

    @staticmethod
    def transform_vec2(points, size, pos):
        result = list()
        for v in points:
            result.append(((v[0] + pos[0]) * size[0],
                           (v[1] + pos[1]) * size[1]))

        return result
