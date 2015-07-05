from color import RGBColor

class Tracer(object):
    def __init__(self, world):
        self.world = world

    def trace_ray(self, ray):
        intersection = self.world.ray_intersection(ray)
        if intersection.is_hit:
            return intersection.color
        return RGBColor.Black()
