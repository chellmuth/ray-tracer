from bbox import BoundingBox
from geometry import Geometry, Intersection
from point import Point3
from vector import Vector3

epsilon = 0.001

class Face(object):
    def __init__(self, vertex_indices, normal_indices):
        self.vertex_indices = vertex_indices
        self.normal_indices = normal_indices

class Mesh(object):
    def __init__(self, vertices, normals, faces):
        self.vertices = vertices
        self.normals = normals
        self.faces = faces

class Triangle(object):
    def __init__(self, mesh, face, material):
        self.mesh = mesh

        self.index0 = face.vertex_indices[0]
        self.index1 = face.vertex_indices[1]
        self.index2 = face.vertex_indices[2]

        self.material = material

    def get_bbox(self):
        p1 = self.mesh.vertices[self.index0]
        p2 = self.mesh.vertices[self.index1]
        p3 = self.mesh.vertices[self.index2]

        return BoundingBox(
            Point3(
                min(p1.x, p2.x, p3.x),
                min(p1.y, p2.y, p3.y),
                min(p1.z, p2.z, p3.z)
            ),
            Point3(
                max(p1.x, p2.x, p3.x),
                max(p1.y, p2.y, p3.y),
                max(p1.z, p2.z, p3.z)
            )
        )

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

        return Intersection.Hit(t, self._interpolate_normal(b1, b2))


class SmoothMeshTriangle(Triangle):
    def __init__(self, mesh, face, material):
        super(SmoothMeshTriangle, self).__init__(mesh, face, material)

        self.normal = Vector3(1.0, 0.0, 0.0)

    def _interpolate_normal(self, beta, gamma):
        interpolated = (
            self.mesh.normals[self.index0].mult(1 - beta - gamma) +
            self.mesh.normals[self.index1].mult(beta) +
            self.mesh.normals[self.index2].mult(gamma)
        )

        return interpolated.normalized()


class FlatMeshTriangle(Triangle):
    def __init__(self, mesh, face, material):
        super(FlatMeshTriangle, self).__init__(mesh, face, material)

        self.normal = sum((mesh.normals[face.normal_indices[i]] for i in range(3)), Vector3.Zero()).normalized()

    def _interpolate_normal(self, beta, gamma):
        return self.normal
