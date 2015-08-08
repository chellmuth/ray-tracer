import math

class Vector3(object):
    @classmethod
    def Zero(cls):
        return cls(0.0, 0.0, 0.0)

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __getitem__(self, key):
        if key == 0: return self.x
        if key == 1: return self.y
        if key == 2: return self.z
        raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise KeyError

    def __repr__(self):
        return "V: (%f, %f, %f)" % (self.x, self.y, self.z)


    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def normalized(self):
        length = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        return Vector3(self.x / length, self.y / length, self.z / length)

    def mult(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def distance(self, other):
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )
