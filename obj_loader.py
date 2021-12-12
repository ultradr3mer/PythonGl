from OpenGL.GL import *


class Obj:
    def __init__(self, filename, swapyz=True, flipy=True):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.plain_vertecies = []
        self.plain_normals = []
        self.plain_texcoords = []

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
                    t = list(map(float, values[1:3]))
                    if flipy:
                        t[1] = 1 - t[1]
                    self.texcoords.append(t)
                elif values[0] in ('usemtl', 'usemat'):
                    material = values[1]
                elif values[0] == 'mtllib':
                    # self.mtl = MTL(values[1])
                    pass
                elif values[0] == 'f':
                    vert = []
                    texcoords = []
                    norms = []
                    for v in values[1:]:
                        w = v.split('/')
                        vert.append(int(w[0]) - 1)
                        if len(w) >= 2 and len(w[1]) > 0:
                            texcoords.append(int(w[1]) - 1)
                        else:
                            texcoords.append(0)
                        if len(w) >= 3 and len(w[2]) > 0:
                            norms.append(int(w[2]) - 1)
                        else:
                            norms.append(0)
                    self.faces.append((vert, norms, texcoords, material))

        for f in self.faces:
            face_indices = f[0]
            vert = (self.vertices[face_indices[0]],
                    self.vertices[face_indices[1]],
                    self.vertices[face_indices[2]])
            self.plain_vertecies.extend(vert)

            norm_indices = f[1]
            norms = (self.normals[norm_indices[0]],
                     self.normals[norm_indices[1]],
                     self.normals[norm_indices[2]])
            self.plain_normals.extend(vert)

            tex_indices = f[2]
            tex = (self.texcoords[tex_indices[0]],
                   self.texcoords[tex_indices[1]],
                   self.texcoords[tex_indices[2]])
            self.plain_texcoords.extend(tex)

    def get_pymunk_vertecies(self):
        result = list()

        for f in self.faces:
            for v_index in f[0]:
                result.append(list(self.vertices[v_index][:2]))

        return result
