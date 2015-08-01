from geometry import Geometry, Intersection
from point import Point3

epsilon = 0.001

class Mesh(object):
    def __init__(self):
        self.vertices = [
            Point3(-2.0, -2.0, -10.0),
            Point3(2.0, -1.0, -10.0),
            Point3(1.0, 2.0, -10.0)
        ]

        self.indices = [ 0, 1, 2 ]


class FlatMeshTriangle(object):
    def __init__(self, mesh, normal, indices, material):
        self.mesh = mesh
        self.index0 = indices[0]
        self.index1 = indices[1]
        self.index2 = indices[2]

        self.normal = normal
        self.material = material

    def intersect(self, ray):
        # pbrt "Triangle Intersection" pp. 140-145
        p1 = self.mesh.vertices[self.index0]
        p2 = self.mesh.vertices[self.index1]
        p3 = self.mesh.vertices[self.index2]

        # compute s1
        e1 = p2 - p1
        e2 = p3 - p1
        s1 = ray.direction.cross(e2)
        divisor = s1.dot(e1)
        if divisor == 0.0:
            return Intersection.Miss()
        inv_divisor = 1.0 / divisor

        # compute first barycentric coordinate
        s = ray.origin - p1
        b1 = s.dot(s1) * inv_divisor
        if b1 < 0.0 or b1 > 1.0:
            return Intersection.Miss()

        # compute second barycentric coordinate
        s2 = s.cross(e1)
        b2 = ray.direction.dot(s2) * inv_divisor
        if b2 < 0.0 or (b1 + b2) > 1.0:
            return Intersection.Miss()

        # compute t intersection point
        t = e2.dot(s2) * inv_divisor

        if t < epsilon:
            return Intersection.Miss()

        return Intersection.Hit(t, self.normal)