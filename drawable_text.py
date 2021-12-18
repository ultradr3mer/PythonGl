from drawable import Drawable
from generated_mesh import GenMesh


def generate_character_map():
    characters = ' !"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    line_length = 12

    result = dict()

    line_number = 0
    while len(characters) > 0:
        line, characters = characters[:line_length], characters[line_length:]

        character_number = 0
        for c in line:
            result[c] = (character_number, line_number)
            character_number += 1

        line_number += 1

    return result


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

    character_map = generate_character_map()

    def __init__(self, shader, text=""):
        self.mesh = GenMesh()
        self.set_text(text)
        super(DrawableText, self).__init__(self.mesh, shader)

    def set_text(self, text):
        verts = list()
        tex_coords = list()

        x_pos = 0
        for current_character in text:
            verts.extend(self.transform_vec3(self.base_verts, pos=(x_pos, 0), size=(36.0 / 64.0, 1.0)))
            tex_coords.extend(self.transform_vec2(self.base_tex_coords,
                                                  size=(36.0 / 512.0, 64.0 / 512.0),
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
