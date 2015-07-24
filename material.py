from brdf import Lambertian
from color import RGBColor
from ray import Ray

class Material(object):
    pass

class Matte(Material):
    def __init__(self, color):
        self.ambient_brdf = Lambertian(color)
        self.diffuse_brdf = Lambertian(color)

    def shade(self, shading_record, world):
        w_out = -shading_record.ray.direction
        L = self.ambient_brdf.rho() * shading_record.ambient_light.L()

        for light in shading_record.lights:
            w_in = light.direction(shading_record.hit_point)
            dot = shading_record.normal.dot(w_in)

            if dot > 0.0:
                shadow_ray = Ray(shading_record.hit_point, w_in)
                if not light.is_shadowed(shadow_ray, world):
                    L += (self.diffuse_brdf.f() * light.L()).mult(dot)

        return L

class Normal(Material):
    def shade(self, shading_record, world):
        normal = shading_record.normal
        r = (normal.x + 1.0) / 2.0
        g = (normal.y + 1.0) / 2.0
        b = (normal.z + 1.0) / 2.0
        return RGBColor(r, g, b)
