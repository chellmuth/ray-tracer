from point import Point3
from vector import Vector3

class Matrix4(object):
    @classmethod
    def Identity(cls):
        return cls(
            [ 1, 0, 0, 0],
            [ 0, 1, 0, 0],
            [ 0, 0, 1, 0],
            [ 0, 0, 0, 1]
        )

    @classmethod
    def Translate(cls, x, y, z):
        return cls(
            [ 1, 0, 0, x],
            [ 0, 1, 0, y],
            [ 0, 0, 1, z],
            [ 0, 0, 0, 1]
        )

    @classmethod
    def Scale(cls, x, y, z):
        return cls(
            [ x, 0, 0, 0],
            [ 0, y, 0, 0],
            [ 0, 0, z, 0],
            [ 0, 0, 0, 1]
        )

    def __init__(self, *rows):
        self.rows = rows

    def mult_point(self, point):
        m = self.rows
        x = m[0][0] * point.x + m[0][1] * point.y + m[0][2] * point.z + m[0][3]
        y = m[1][0] * point.x + m[1][1] * point.y + m[1][2] * point.z + m[1][3]
        z = m[2][0] * point.x + m[2][1] * point.y + m[2][2] * point.z + m[2][3]
        return Point3(x, y, z)

    def mult_vector(self, vector):
        m = self.rows
        x = m[0][0] * vector.x + m[0][1] * vector.y + m[0][2] * vector.z
        y = m[1][0] * vector.x + m[1][1] * vector.y + m[1][2] * vector.z
        z = m[2][0] * vector.x + m[2][1] * vector.y + m[2][2] * vector.z
        return Vector3(x, y, z)
