class Vector3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    # def mult(self, scalar):
    #     return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
