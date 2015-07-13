from color import RGBColor

class Tracer(object):
    def __init__(self, world):
        self.world = world

    def trace_ray(self, ray):
        result = self.world.ray_intersection(ray)
        if result.intersection.is_hit:
            return result.shading_record.material.shade(result.shading_record)

        return self.world.background_color

class TraceResult(object):
    def __init__(self, intersection, shading_record):
        self.intersection = intersection
        self.shading_record = shading_record

class ShadingRecord(object):
    def __init__(self, ambient_light, lights, material, normal, ray, hit_point):
        self.ambient_light = ambient_light
        self.lights = lights
        self.material = material
        self.normal = normal
        self.ray = ray
        self.hit_point = hit_point
