import math
import numpy
import scipy.misc

from camera import Camera
from color import RGBColor
from geometry import Disk, Sphere, OpenCylinder, Intersection
from instance import Instance
from light import AmbientLight, PointLight
from loader import load_obj
from material import Matte, Phong, Normal
from mesh import Mesh, FlatMeshTriangle
from point import Point3
from sampler import Sampler
from tracer import Tracer, TraceResult, ShadingRecord
from vector import Vector3

class World(object):
    def __init__(self):
        self.tracer = Tracer(self)
        self.sampler = Sampler(1)
        self.view_plane = ViewPlane()
        self.background_color = RGBColor(0.1, 0.1, 0.1)
        self.camera = Camera()
        self.geometry = []
        self.data = numpy.zeros((self.view_plane.vres, self.view_plane.hres, 3), dtype=numpy.uint8)

        mesh = load_obj("teapot.obj")
        for face in mesh.faces:
            triangle = FlatMeshTriangle(mesh, face, material=Phong(RGBColor.Red()))
            # triangle.scale(3.5, 3.5, 3.5)
            # triangle.rotate_y(-math.pi / 10)
            # triangle.translate(-1.3, 3.5, -25.0)
            self.add_geometry(triangle)

        self.ambient_light = AmbientLight()
        self.lights = [ PointLight(Point3(8.0, 2.0, 5.0)) ]

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
