from math import cos, sin

from point import Point3
from vector import Vector3

class Matrix4(object):
    @classmethod
    def Identity(cls):
        return cls(
            [ 1, 0, 0, 0 ],
            [ 0, 1, 0, 0 ],
            [ 0, 0, 1, 0 ],
            [ 0, 0, 0, 1 ]
        )

    @classmethod
    def Translate(cls, x, y, z):
        return cls(
            [ 1, 0, 0, x ],
            [ 0, 1, 0, y ],
            [ 0, 0, 1, z ],
            [ 0, 0, 0, 1 ]
        )

    @classmethod
    def Scale(cls, x, y, z):
        return cls(
            [ x, 0, 0, 0 ],
            [ 0, y, 0, 0 ],
            [ 0, 0, z, 0 ],
            [ 0, 0, 0, 1 ]
        )

    @classmethod
    def RotateX(cls, theta):
        return cls(
            [ 1, 0, 0, 0 ],
            [ 0, cos(theta), -sin(theta), 0 ],
            [ 0, sin(theta), cos(theta), 0 ],
            [ 0, 0, 0, 1 ]
        )

    @classmethod
    def RotateY(cls, theta):
        return cls(
            [ cos(theta), 0, -sin(theta), 0 ],
            [ 0, 1, 0, 0 ],
            [ sin(theta), 0, cos(theta), 0 ],
            [ 0, 0, 0, 1 ]
        )

    @classmethod
    def RotateZ(cls, theta):
        return cls(
            [ cos(theta), -sin(theta), 0, 0 ],
            [ sin(theta), cos(theta), 0, 0 ],
            [ 0, 0, 1, 0 ],
            [ 0, 0, 0, 1 ]
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

    def __mul__(self, other):
        m = self.rows
        n = other.rows
        return Matrix4(
            [
                m[0][0] * n[0][0] + m[0][1] * n[1][0] + m[0][2] * n[2][0] + m[0][3] * n[3][0],
                m[0][0] * n[0][1] + m[0][1] * n[1][1] + m[0][2] * n[2][1] + m[0][3] * n[3][1],
                m[0][0] * n[0][2] + m[0][1] * n[1][2] + m[0][2] * n[2][2] + m[0][3] * n[3][2],
                m[0][0] * n[0][3] + m[0][1] * n[1][3] + m[0][2] * n[2][3] + m[0][3] * n[3][3],
            ],
            [
                m[1][0] * n[0][0] + m[1][1] * n[1][0] + m[1][2] * n[2][0] + m[1][3] * n[3][0],
                m[1][0] * n[0][1] + m[1][1] * n[1][1] + m[1][2] * n[2][1] + m[1][3] * n[3][1],
                m[1][0] * n[0][2] + m[1][1] * n[1][2] + m[1][2] * n[2][2] + m[1][3] * n[3][2],
                m[1][0] * n[0][3] + m[1][1] * n[1][3] + m[1][2] * n[2][3] + m[1][3] * n[3][3],
            ],
            [
                m[2][0] * n[0][0] + m[2][1] * n[1][0] + m[2][2] * n[2][0] + m[2][3] * n[3][0],
                m[2][0] * n[0][1] + m[2][1] * n[1][1] + m[2][2] * n[2][1] + m[2][3] * n[3][1],
                m[2][0] * n[0][2] + m[2][1] * n[1][2] + m[2][2] * n[2][2] + m[2][3] * n[3][2],
                m[2][0] * n[0][3] + m[2][1] * n[1][3] + m[2][2] * n[2][3] + m[2][3] * n[3][3],
            ],
            [
                m[3][0] * n[0][0] + m[3][1] * n[1][0] + m[3][2] * n[2][0] + m[3][3] * n[3][0],
                m[3][0] * n[0][1] + m[3][1] * n[1][1] + m[3][2] * n[2][1] + m[3][3] * n[3][1],
                m[3][0] * n[0][2] + m[3][1] * n[1][2] + m[3][2] * n[2][2] + m[3][3] * n[3][2],
                m[3][0] * n[0][3] + m[3][1] * n[1][3] + m[3][2] * n[2][3] + m[3][3] * n[3][3],
            ]
        )

    def __repr__(self):
        return "\n".join(" ".join(str(self.rows[row][col]) for col in range(4)) for row in range(4))
