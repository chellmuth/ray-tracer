import color
import math

from bbox import BoundingBox
from matrix import Matrix4
from point import Point3
from vector import Vector3

epsilon = 0.001

class Intersection(object):
    @classmethod
    def Miss(cls):
        return cls(False, float('inf'), None, None)

    @classmethod
    def Hit(cls, t, normal, material):
        return cls(True, t, normal, material)

    def __init__(self, is_hit, t, normal, material):
        self.is_hit = is_hit
        self.t = t
        self.normal = normal
        self.material = material

    def is_closer(self, other):
        return self.t < other.t


class Geometry(object):
    def __init__(self):
        self.casts_shadows = True

    def shadow_intersect(self, ray):
        if self.casts_shadows:
            return self.intersect(ray)
        else:
            return Intersection.Miss()


class Sphere(Geometry):
    def __init__(self, center, radius, material):
        super(Sphere, self).__init__()

        self.center = center
        self.radius = radius
        self.material = material

    def get_bbox(self):
        return BoundingBox(
            Point3(
                self.center.x - self.radius,
                self.center.y - self.radius,
                self.center.z - self.radius
             ),
            Point3(
                self.center.x + self.radius,
                self.center.y + self.radius,
                self.center.z + self.radius
            )
        )

    def intersect(self, ray):
        temp = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = temp.dot(ray.direction) * 2.0
        c = temp.dot(temp) - (self.radius * self.radius)
        disc = b * b - 4.0 * a * c

        if disc < 0.0:
            return Intersection.Miss()

        e = math.sqrt(disc)
        denom = 2.0 * a
        t = (-b - e) / denom

        if t > epsilon:
            normal = (temp + ray.direction.mult(t)).normalized()
            return Intersection.Hit(t, normal, self.material)

        t = (-b + e) / denom
        if t > epsilon:
            normal = (temp + ray.direction.mult(t)).normalized()
            return Intersection.Hit(t, normal, self.material)

        return Intersection.Miss()

    def __repr__(self):
        return "C: (%s), r: %s" % (self.center, self.radius)


class Disk(Geometry):
    def __init__(self, center, normal, radius, material):
        self.center = center
        self.normal = normal
        self.radius = radius
        self.material = material

    def get_bbox(self):
        return BoundingBox(
            Point3(
                self.center.x - self.radius,
                self.center.y - self.radius,
                -epsilon
            ),
            Point3(
                self.center.x + self.radius,
                self.center.y + self.radius,
                epsilon
            )
        )

    def intersect(self, ray):
        # plug (o + td) ray into (p - a) * n = 0 plane equation
        # (o + td - a) * n = 0
        # t = (a - o) * n / (d * n)
        t = (self.center - ray.origin).dot(self.normal) / ray.direction.dot(self.normal)

        if t <= epsilon: return Intersection.Miss()

        if self.center.squared_distance(ray.extrapolate(t)) < self.radius ** 2:
            return Intersection.Hit(t, self.normal, self.material)

        return Intersection.Miss()


class OpenCylinder(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersect(self, ray):
        # plug (o + td) ray into x^2 + z^2 - r^2 = 0

        temp = ray.origin - self.center
        temp.y = 0.0
        a = ray.direction.x ** 2 + ray.direction.z ** 2
        b = temp.dot(ray.direction) * 2.0
        c = temp.dot(temp) - (self.radius * self.radius)
        disc = b * b - (4.0 * a * c)

        if disc < 0.0:
            return Intersection.Miss()

        e = math.sqrt(disc)
        denom = 2.0 * a
        t = (-b - e) / denom

        if t > epsilon:
            hit = ray.extrapolate(t)
            normal = Vector3(hit.x - self.center.x, 0, hit.z - self.center.z).normalized()
            return Intersection.Hit(t, normal, self.material)

        t = (-b + e) / denom
        if t > epsilon:
            hit = ray.extrapolate(t)
            normal = Vector3(hit.x - self.center.x, 0, hit.z - self.center.z).normalized()
            return Intersection.Hit(t, normal, self.material)

        return Intersection.Miss()

# class Plane(Geometry):
#     def __init__(self, point, normal):
#         self.point = point
#         self.normal = normal

#     def is_hit(self, ray):
#         t = (self.point - ray.origin).dot(self.normal) / ray.direction.dot(self.normal)

#         if t > epsilon:
#             return Intersection.Hit(t)

#         return Intersection.Miss()
