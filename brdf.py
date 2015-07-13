import math

from color import RGBColor

class BRDF(object):
    pass

class Lambertian(BRDF):
    def __init__(self, color):
        self.diffuse_reflection = 1.0
        self.diffuse_color = color

    def f(self):
        return self.diffuse_color.mult(self.diffuse_reflection / math.pi)

    # bihemisherical reflectance
    def rho(self):
        return self.diffuse_color.mult(self.diffuse_reflection)
