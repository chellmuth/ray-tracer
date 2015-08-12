from bbox import BoundingBox
from geometry import Geometry
from matrix import Matrix4
from point import Point3

class Instance(Geometry):
    def __init__(self, geometry):
        super(Instance, self).__init__()

        self.geometry = geometry
        self.inverse = Matrix4.Identity()
        self.forward = Matrix4.Identity()

    def get_bbox(self):
        points = self.geometry.get_bbox().points
        transformed_points = [
            self.forward.mult_point(point)
            for point in points
        ]

        p0 = Point3(
            min(p.x for p in transformed_points),
            min(p.y for p in transformed_points),
            min(p.z for p in transformed_points)
        )
        p1 = Point3(
            max(p.x for p in transformed_points),
            max(p.y for p in transformed_points),
            max(p.z for p in transformed_points)
        )
        return BoundingBox(p0, p1)

    @property
    def material(self):
        return self.geometry.material

    def translate(self, x, y, z):
        self.forward = Matrix4.Translate(x, y, z) * self.forward
        self.inverse = self.inverse * Matrix4.Translate(-x, -y, -z)

    def scale(self, x, y, z):
        self.forward = Matrix4.Scale(x, y, z) * self.forward
        self.inverse = self.inverse * Matrix4.Scale(1.0/x, 1.0/y, 1.0/z)

    def rotate_x(self, theta):
        self.forward = Matrix4.RotateX(theta) * self.forward
        self.inverse = self.inverse * Matrix4.RotateX(-theta)

    def rotate_y(self, theta):
        self.forward = Matrix4.RotateY(theta) * self.forward
        self.inverse = self.inverse * Matrix4.RotateY(-theta)

    def rotate_z(self, theta):
        self.forward = Matrix4.RotateZ(theta) * self.forward
        self.inverse = self.inverse * Matrix4.RotateZ(-theta)

    def intersect(self, ray):
        transformed_ray = ray.transform(self.inverse)
        intersection = self.geometry.intersect(transformed_ray)
        if intersection.is_hit:
            intersection.normal = self.inverse.mult_vector(intersection.normal).normalized()

        return intersection
