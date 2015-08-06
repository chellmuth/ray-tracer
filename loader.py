import re

from mesh import Mesh, Face
from point import Point3
from vector import Vector3

def load_obj(filename):
    vertices = []
    normals = [Vector3(0.0, 0.0, 1.0)]
    faces = []

    f = open(filename, "r")
    for line in f.readlines():
        match = re.match("^v +([^ ]+) ([^ ]+) ([^ ]+)$\s*", line)
        if match:
            vertices.append(Point3(*[ float(match.group(i)) for i in range(1, 4)]))

        match = re.match("^vn +([^ ]+) ([^ ]+) ([^ ]+)\s*$", line)
        if match:
            normals.append(Vector3(*[ float(match.group(i)) for i in range(1, 4)]))

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
                face_vertices = []
                face_normals = []

                for index in face_triple:
                    group = match.group(index)
                    vertex_index = uv_index = normal_index = None
                    try:
                        vertex_index, uv_index, normal_index = [ int(i) for i in group.split("/") ]
                    except:
                        vertex_index, normal_index = [ int(i) for i in group.split("/") ]
                    if vertex_index > 0:
                        vertex_index -= 1
                    face_vertices.append(vertex_index)
                    face_normals.append(0)

                faces.append(Face(face_vertices, face_normals))

    # 15704 faces
    return Mesh(vertices, normals, faces[:5000])
