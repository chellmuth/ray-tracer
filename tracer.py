from color import RGBColor

class Tracer(object):
    def __init__(self, world):
        self.world = world

    def trace_ray(self, ray):
        intersection =  self.world.sphere.intersect(ray)
        if intersection.is_hit:
            return RGBColor.Red()
        return RGBColor.Black()
