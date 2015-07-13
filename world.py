import numpy
import scipy.misc

from camera import Camera
from color import RGBColor
from geometry import Sphere, Intersection
from light import AmbientLight, PointLight
from material import Matte
from point import Point3
from sampler import Sampler
from tracer import Tracer, TraceResult, ShadingRecord
from vector import Vector3

class World(object):
    def __init__(self):
        self.tracer = Tracer(self)
        self.sampler = Sampler(25)
        self.view_plane = ViewPlane()
        self.background_color = RGBColor(0.1, 0.1, 0.1)
        self.camera = Camera()
        self.geometry = []
        self.data = numpy.zeros((self.view_plane.vres, self.view_plane.hres, 3), dtype=numpy.uint8)

        sphere1 = Sphere(Point3(150.0, 0.0, -1200.0), 100.0, Matte(RGBColor.Blue()))
        sphere2 = Sphere(Point3(0.0, -100.0, -800.0), 100.0, Matte(RGBColor.Red()))
        self.add_geometry(sphere1)
        self.add_geometry(sphere2)

        self.ambient_light = AmbientLight()
        self.lights = [ PointLight(Point3(0.0, 200.0, -200.0)) ]

    def add_geometry(self, geometry):
        self.geometry.append(geometry)

    def render_scene(self):
        self.camera.render_scene(self)

    def ray_intersection(self, ray):
        closest_hit = TraceResult(Intersection.Miss(), None)
        for geometry in self.geometry:
            intersection = geometry.intersect(ray)
            if intersection.is_hit and intersection.is_closer(closest_hit.intersection):
                shading_record = ShadingRecord(self.ambient_light, self.lights, geometry.material, intersection.normal, ray, ray.extrapolate(intersection.t))
                closest_hit = TraceResult(intersection, shading_record)

        return closest_hit

    def display_pixel(self, row, col, color):
        self.data[row, col] = color.to_list()

    def show(self):
        image = scipy.misc.toimage(self.data)
        image.show()

class ViewPlane(object):
    def __init__(self):
        self.hres = 200
        self.vres = 200
        self.pixel_size = 1.0
