import numpy as np

epsilon = 0.001

class BoundingBox(object):
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1


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
