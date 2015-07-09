import numpy
import scipy.misc

from camera import Camera
from color import RGBColor
from geometry import Sphere, Intersection
from point import Point3
from sampler import Sampler
from tracer import Tracer
from vector import Vector3

class World(object):
    def __init__(self):
        self.tracer = Tracer(self)
        self.sampler = Sampler(25)
        self.view_plane = ViewPlane()
        self.camera = Camera()
        self.geometry = []
        self.data = numpy.zeros((self.view_plane.vres, self.view_plane.hres, 3), dtype=numpy.uint8 )

        self.add_geometry(Sphere(Point3(150.0, 0.0, -1200.0), 100.0, RGBColor.Blue()))
        self.add_geometry(Sphere(Point3(0.0, -100.0, -800.0), 100.0, RGBColor.Red()))

    def add_geometry(self, geometry):
        self.geometry.append(geometry)

    def render_scene(self):
        self.camera.render_scene(self)

    def ray_intersection(self, ray):
        closest_intersection = Intersection.Miss()
        for geometry in self.geometry:
            intersection = geometry.intersect(ray)
            if intersection.is_hit and intersection.is_closer(closest_intersection):
                closest_intersection = intersection
        return closest_intersection

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
