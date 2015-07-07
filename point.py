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

    def __add__(self, other):
        return Point3(self.x + other.x, self.y + other.x, self.z + other.z)

    def __sub__(self, other):
        return Point3(self.x - other.x, self.y - other.x, self.z - other.z)
