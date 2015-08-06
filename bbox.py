import numpy as np

from point import Point3

epsilon = 0.001

class BoundingBox(object):
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

    def union(self, other):
        return BoundingBox(
            Point3(
                min(self.p0.x, other.p0.x),
                min(self.p0.y, other.p0.y),
                min(self.p0.z, other.p0.z)
            ),
            Point3(
                max(self.p1.x, other.p1.x),
                max(self.p1.y, other.p1.y),
                max(self.p1.z, other.p1.z)
            )
        )

    def grow_epsilon(self):
        return BoundingBox(
            Point3(self.p0.x - epsilon, self.p0.y - epsilon, self.p0.z - epsilon),
            Point3(self.p1.x + epsilon, self.p1.y + epsilon, self.p1.z + epsilon)
        )

    def is_inside(self, point):
        for axis in range(3):
            if self.p0.x <= point.x <= self.p1.x:
                continue
            return False
        return True


    def is_hit(self, ray):
        t0 = epsilon
        t1 = float("inf")

        for axis in range(3):
            # use numpy for IEEE 754 divide-by-zero semantics
            inv_ray_direction = np.divide(1.0, ray.direction[axis])
            t_near = (self.p0[axis] - ray.origin[axis]) * inv_ray_direction
            t_far  = (self.p1[axis] - ray.origin[axis]) * inv_ray_direction

            if t_near > t_far:
                t_near, t_far = t_far, t_near
            t0 = max(t_near, t0)
            t1 = min(t_far, t1)

            if t0 > t1:
                return False
        return True

    def __repr__(self):
        return "p0: %s, p1; %s" % (self.p0, self.p1)
