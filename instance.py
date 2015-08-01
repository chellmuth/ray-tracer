from geometry import Geometry
from matrix import Matrix4

class Instance(Geometry):
    def __init__(self, geometry):
        self.geometry = geometry
        self.inverse = Matrix4.Identity()

    @property
    def material(self):
        return self.geometry.material

    def translate(self, x, y, z):
        self.inverse = self.inverse * Matrix4.Translate(-x, -y, -z)

    def scale(self, x, y, z):
        self.inverse = self.inverse * Matrix4.Scale(1.0/x, 1.0/y, 1.0/z)

    def rotate_x(self, theta):
        self.inverse = self.inverse * Matrix4.RotateX(-theta)

    def rotate_y(self, theta):
        self.inverse = self.inverse * Matrix4.RotateY(-theta)

    def rotate_z(self, theta):
        self.inverse = self.inverse * Matrix4.RotateZ(-theta)

    def intersect(self, ray):
        transformed_ray = ray.transform(self.inverse)
        intersection = self.geometry.intersect(transformed_ray)
        if intersection.is_hit:
            intersection.normal = self.inverse.mult_vector(intersection.normal).normalized()

        return intersection
