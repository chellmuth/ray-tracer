import math

from vector import Vector3

class Point2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(%f, %f)" % (self.x, self.y)

class Point3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalized(self):
        length = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        return Vector3(self.x / length, self.y / length, self.z / length)

    def distance(self, point):
        return math.sqrt(self.squared_distance(point))

    def squared_distance(self, point):
        return (self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2

    def __getitem__(self, key):
        if key == 0: return self.x
        if key == 1: return self.y
        if key == 2: return self.z
        raise KeyError

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __repr__(self):
        return "(%f, %f, %f)" % (self.x, self.y, self.z)
