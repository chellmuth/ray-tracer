from color import RGBColor

class Light(object):
    def __init__(self):
        self.color = RGBColor.White()
        self.radiance_scaling = 1.0


class AmbientLight(Light):
    def __init__(self):
        super(AmbientLight, self).__init__()
        self.radiance_scaling = 0.25

    def direction(self, intersection):
        raise Exception("Should never call direction on AmbientLight")

    def L(self):
        return self.color.mult(self.radiance_scaling)


class PointLight(Light):
    def __init__(self, location):
        super(PointLight, self).__init__()
        self.location = location

    def is_shadowed(self, ray, world):
        distance = self.location.distance(ray.origin)
        for geometry in world.geometry:
            intersection = geometry.intersect(ray)
            if intersection.is_hit and intersection.t < distance:
                return True
        return False

    def direction(self, towards_point):
        return (self.location - towards_point).normalized()

    def L(self):
        return self.color.mult(self.radiance_scaling)
