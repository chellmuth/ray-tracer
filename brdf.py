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

class GlossySpecular(BRDF):
    def __init__(self):
        self.exp = 40.0

    def f(self, shading_record, w_out, w_in):
        n_dot_w_in = shading_record.normal.dot(w_in)
        r = -w_in + shading_record.normal.mult(2.0 * n_dot_w_in)
        r_dot_w_out = r.dot(w_out)
        if r_dot_w_out > 0.0:
            return RGBColor.White().mult(math.pow(r_dot_w_out, self.exp))

        return RGBColor.Black()
