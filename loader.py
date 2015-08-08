import re

from mesh import Mesh, Face
from point import Point3
from vector import Vector3

def load_obj(filename):
    builder = MeshBuilder()
    vertices = []
    normals = []
    faces = []

    f = open(filename, "r")
    for line in f.readlines():
        match = re.match("^v +([^ ]+) ([^ ]+) ([^ ]+)$\s*", line)
        if match:
            builder.parse_vertex(Point3(*[ float(match.group(i)) for i in range(1, 4)]))

        match = re.match("^vn +([^ ]+) ([^ ]+) ([^ ]+)\s*$", line)
        if match:
            builder.parse_normal(Vector3(*[ float(match.group(i)) for i in range(1, 4)]))

        face_triples = []
        match = re.match("^f +([^ ]+) ([^ ]+) ([^ ]+)\s*$", line)
        if match:
            face_triples = [ (1, 2, 3) ]
        else:
            match = re.match("^f +([^ ]+) ([^ ]+) ([^ ]+) ([^ ]+)\s*$", line)
            if match:
                face_triples = [ (1, 2, 3), (3, 4, 1) ]


        if face_triples:
            for face_triple in face_triples:
                face_vertex_indices = []

                for index in face_triple:
                    group = match.group(index)
                    vertex_index = uv_index = normal_index = None
                    try:
                        vertex_index, uv_index, normal_index = [ int(i) for i in group.split("/") ]
                    except:
                        vertex_index, uv_index = [ int(i) for i in group.split("/") ]
                    if vertex_index > 0:
                        vertex_index -= 1
                    face_vertex_indices.append(vertex_index)

                builder.parse_face(*face_vertex_indices)

    # 15704 faces
    return builder.to_mesh()

class FaceBuilder(object):
    def __init__(self, i1, i2,i3):
        self.index1 = i1
        self.index2 = i2
        self.index3 = i3

    @property
    def indices(self):
        return [self.index1, self.index2, self.index3]

    def normal(self, vertices):
        v = vertices[self.index2] - vertices[self.index1]
        w = vertices[self.index3] - vertices[self.index1]
        return v.cross(w)

class MeshBuilder(object):
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.faces = []

    def parse_vertex(self, p):
        self.vertices.append(p)

    def parse_normal(self, v):
        self.normals.append(v)

    def parse_face(self, i1, i2, i3):
        self.faces.append(FaceBuilder(i1, i2, i3))

    def to_mesh(self, limit=None):
        limit = limit or len(self.faces)
        self._finish()
        return Mesh(self.vertices, self.normals, self.faces[:limit])

    def _finish(self):
        self._calculate_vertex_normals()
        self._create_face_objects()

    def _calculate_vertex_normals(self):
        normal_accumulator = [ Vector3.Zero() for _ in self.vertices ]
        for face in self.faces:
            face_normal = face.normal(self.vertices)

            normal_accumulator[face.index1] += face_normal
            normal_accumulator[face.index2] += face_normal
            normal_accumulator[face.index3] += face_normal

        self.normals = [ na.normalized() for na in normal_accumulator ]

    def _create_face_objects(self):
        self.faces = [ Face(f.indices, f.indices) for f in self.faces ]
