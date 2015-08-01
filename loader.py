import re

from mesh import Mesh, Face
from point import Point3
from vector import Vector3

def load_obj(filename):
    vertices = []
    normals = []
    faces = []

    f = open(filename, "r")
    for line in f.readlines():
        match = re.match("^v ([^ ]+) ([^ ]+) ([^ ]+)$", line)
        if match:
            vertices.append(Point3(*[ float(match.group(i)) for i in range(1, 4)]))

        match = re.match("^vn ([^ ]+) ([^ ]+) ([^ ]+)$", line)
        if match:
            normals.append(Vector3(*[ float(match.group(i)) for i in range(1, 4)]))

        match = re.match("^f ([^ ]+) ([^ ]+) ([^ ]+)$", line)
        if match:
            face_vertices = []
            face_normals = []
            for index in range(1, 4):
                group = match.group(index)
                vertex_index, uv_index, normal_index = [ int(i) for i in group.split("/") ]
                face_vertices.append(vertex_index)
                face_normals.append(normal_index)
            faces.append(Face(face_vertices, face_normals))

    return Mesh(vertices, normals, faces)
