import numpy
import scipy.misc

from geometry import Sphere
from point import Point3
from ray import Ray
from tracer import Tracer
from vector import Vector3

class World(object):
    def __init__(self):
        self.tracer = Tracer(self)
        self.view_plane = ViewPlane()
        self.sphere = Sphere(Point3(0.0, 0.0, 0.0), 85.0)
        self.data = numpy.zeros((self.view_plane.vres, self.view_plane.hres, 3), dtype=numpy.uint8 )

    def render_scene(self):
        zw = 100.0

        hres = self.view_plane.hres
        vres = self.view_plane.vres
        pixel_size = self.view_plane.pixel_size
        for row in range(hres):
            for col in range(vres):
                x = pixel_size * (col - 0.5 * (hres - 1.0))
                y = pixel_size * (row - 0.5 * (vres - 1.0))

                ray = Ray(Point3(x, y, zw), Vector3(0, 0, -1))
                color = self.tracer.trace_ray(ray)
                self.display_pixel(row, col, color)

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
