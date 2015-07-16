import color
import math

from vector import Vector3

epsilon = 0.001

class Intersection(object):
    @classmethod
    def Miss(cls):
        return cls(False, float('inf'), None)

    @classmethod
    def Hit(cls, t, normal):
        return cls(True, t, normal)

    def __init__(self, is_hit, t, normal):
        self.is_hit = is_hit
        self.t = t
        self.normal = normal

    def is_closer(self, other):
        return self.t < other.t


class Geometry(object):
    pass


class Sphere(Geometry):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

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
            return Intersection.Hit(t, normal)

        t = (-b + e) / denom
        if t > epsilon:
            normal = (temp + ray.direction.mult(t)).normalized()
            return Intersection.Hit(t, normal)

        return Intersection.Miss()

class Disk(Geometry):
    def __init__(self, center, normal, radius, material):
        self.center = center
        self.normal = normal
        self.radius = radius
        self.material = material

    def intersect(self, ray):
        # plug (o + td) ray into (p - a) * n = 0 plane equation
        # (o + td - a) * n = 0
        # t = (a - o) * n / (d * n)
        t = (self.center - ray.origin).dot(self.normal) / ray.direction.dot(self.normal)

        if t <= epsilon: return Intersection.Miss()

        if self.center.squared_distance(ray.extrapolate(t)) < self.radius ** 2:
            return Intersection.Hit(t, self.normal)

        return Intersection.Miss()


class OpenCylinder(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersect(self, ray):
        # plug (o + td) ray into x^2 + z^2 - r^2 = 0

        a = ray.direction.x ** 2 + ray.direction.z ** 2
        b = 2 * ((ray.direction.x * (ray.origin.x - self.center.x)) + (ray.direction.z * (ray.origin.z - self.center.z)))
        c = (ray.origin.x - self.center.x) ** 2 + (ray.origin.z - self.center.z) ** 2 - self.radius ** 2
        disc = b * b - (4.0 * a * c)

        if disc < 0.0:
            return Intersection.Miss()

        e = math.sqrt (disc)
        denom = 2.0 * a
        t = (-b - e) / denom

        if t > epsilon:
            hit = ray.extrapolate(t)
            normal = Vector3(-hit.x / self.radius, 0, -hit.z / self.radius).normalized()
            return Intersection.Hit(t, normal)

        t = (-b + e) / denom
        if t > epsilon:
            hit = ray.extrapolate(t)
            normal = Vector3(-hit.x / self.radius, 0, -hit.z / self.radius).normalized()
            return Intersection.Hit(t, normal)

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
