import numpy
import scipy.misc

from color import RGBColor
from geometry import Sphere, Intersection
from point import Point3
from ray import Ray
from sampler import Sampler
from tracer import Tracer
from vector import Vector3

class World(object):
    def __init__(self):
        self.tracer = Tracer(self)
        self.sampler = Sampler(25)
        self.view_plane = ViewPlane()
        self.geometry = []
        self.data = numpy.zeros((self.view_plane.vres, self.view_plane.hres, 3), dtype=numpy.uint8 )

        # self.add_geometry(Sphere(Point3(0.0, 0.0, 0.0), 85.0, RGBColor.Blue()))
        # self.add_geometry(Sphere(Point3(20.0, 20.0, 200.0), 35.0, RGBColor.Red()))

        self.add_geometry(Sphere(Point3(-20.0, 0.0, 0.0), 55.0, RGBColor.Blue()))
        self.add_geometry(Sphere(Point3(0.0, 20.0, 0.0), 45.0, RGBColor.Red()))

    def add_geometry(self, geometry):
        self.geometry.append(geometry)

    def render_scene(self):
        zw = 100.0

        hres = self.view_plane.hres
        vres = self.view_plane.vres
        pixel_size = self.view_plane.pixel_size
        for row in range(hres):
            for col in range(vres):
                color = RGBColor.Black()
                samples = self.sampler.generate_samples()
                for sample in samples:
                    x = pixel_size * (col - 0.5 * hres + sample.x)
                    y = pixel_size * (row - 0.5 * vres + sample.y)

                    ray = Ray(Point3(x, y, zw), Vector3(0, 0, -1))
                    color += self.tracer.trace_ray(ray)

                color /= len(samples)

                self.display_pixel(row, col, color)

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
