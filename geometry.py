import color
import math

epsilon = 0.001

class Geometry(object):
    def __init__(self):
        self.color = color.RGBColor()


class Intersection(object):
    @classmethod
    def Miss(cls):
        return cls(False, None)

    @classmethod
    def Hit(cls, t):
        return cls(True, t)

    def __init__(self, is_hit, t):
        self.is_hit = is_hit
        self.t = t


class Sphere(Geometry):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

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
            return Intersection.Hit(t)

        t = (-b + e) / denom
        if t > epsilon:
            return Intersection.Hit(t)

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
