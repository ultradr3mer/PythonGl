from OpenGL.GL import *


class Obj:
    def __init__(self, filename, swapyz=True, flipy=True):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        material = None
        with open(filename, "r") as file:
            for line in file:
                if line.startswith('#'):
                    continue
                values = line.split()
                if not values:
                    continue
                if values[0] == 'v':
                    v = list(map(float, values[1:4]))
                    if swapyz:
                        v = [v[0], v[2], v[1]]
                    if flipy:
                        v[1] *= -1
                    self.vertices.append(v)
                elif values[0] == 'vn':
                    v = list(map(float, values[1:4]))
                    if swapyz:
                        v = [v[0], v[2], v[1]]
                    if flipy:
                        v[1] *= -1
                    self.normals.append(list(v))
                elif values[0] == 'vt':
                    self.texcoords.append(list(map(float, values[1:3])))
                elif values[0] in ('usemtl', 'usemat'):
                    material = values[1]
                elif values[0] == 'mtllib':
                    # self.mtl = MTL(values[1])
                    pass
                elif values[0] == 'f':
                    face = []
                    texcoords = []
                    norms = []
                    for v in values[1:]:
                        w = v.split('/')
                        face.append(int(w[0]) - 1)
                        if len(w) >= 2 and len(w[1]) > 0:
                            texcoords.append(int(w[1]) - 1)
                        else:
                            texcoords.append(0)
                        if len(w) >= 3 and len(w[2]) > 0:
                            norms.append(int(w[2]) - 1)
                        else:
                            norms.append(0)
                    self.faces.append((face, norms, texcoords, material))

    def get_vertecies(self):
        result = list()

        for v in self.vertices:
            result.extend(v)

        return result

    def get_indices(self):
        result = list()

        for f in self.faces:
            result.extend(f[0])

        return result

    def get_plain_vertecies(self) -> list[float]:
        result = list()

        for f in self.faces:
            for v_index in f[0]:
                result.extend(self.vertices[v_index])

        return result

    def get_pymunk_vertecies(self):
        result = list()

        for f in self.faces:
            for v_index in f[0]:
                result.append(list(self.vertices[v_index][:2]))

        return result

