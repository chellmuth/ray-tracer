import re

from mesh import Mesh
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
            face = []
            for index in range(1, 4):
                group = match.group(index)
                face.append(int(group.split("/")[0]))
            faces.append(face)

    return Mesh(vertices, normals, faces)
