from brdf import Lambertian

class Material(object):
    pass

class Matte(Material):
    def __init__(self, color):
        self.ambient_brdf = Lambertian(color)
        self.diffuse_brdf = Lambertian(color)

    def shade(self, shading_record):
        w_out = -shading_record.ray.direction
        L = self.ambient_brdf.rho() * shading_record.ambient_light.L()

        for light in shading_record.lights:
            w_in = light.direction(shading_record.hit_point)
            dot = shading_record.normal.dot(w_in)

            if dot > 0.0:
                L += (self.diffuse_brdf.f() * light.L()).mult(dot)

        return L
