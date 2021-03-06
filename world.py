import math

import numpy
import scipy.misc

from camera import Camera
from color import RGBColor
from geometry import Disk, Sphere, OpenCylinder, Intersection
from grid import Grid
from instance import Instance
from light import AmbientLight, PointLight
from loader import load_obj
from material import Matte, Phong, Normal, Distance, Emissive
from mesh import Mesh, FlatMeshTriangle, SmoothMeshTriangle
from point import Point3
from sampler import Sampler
from tracer import Tracer, TraceResult, ShadingRecord
from vector import Vector3

class World(object):
    def __init__(self, config):
        self.tracer = Tracer(self)
        self.sampler = Sampler(config.samples)
        self.view_plane = ViewPlane()
        self.background_color = RGBColor(0.1, 0.1, 0.1)
        self.camera = Camera()
        self.geometry = []
        self.lights = []
        self.data = numpy.zeros((self.view_plane.vres, self.view_plane.hres, 3), dtype=numpy.uint8)

        mesh = load_obj("teapot.obj")
        triangles = []
        if config.debug:
            for face in mesh.faces:
                triangle = SmoothMeshTriangle(mesh, face, material=Phong(RGBColor.Red()))
                self.add_geometry(triangle)

        else:
            for face in mesh.faces:
                triangle = Instance(SmoothMeshTriangle(mesh, face, material=Normal()))
                triangle.scale(0.02, 0.02, 0.02)
                triangle.rotate_y(math.pi/10.0)
                triangle.translate(-1, -1.2, -5)
                triangles.append(triangle)

            disk = Instance(Disk(Point3(0, 0, 0), Vector3(0, 0, 1), 5, material=Matte(RGBColor(0.9, 0.9, 0.9))))
            disk.translate(0, 0, -8)

            self.add_geometry(disk)

            # sphere = Instance(Sphere(Point3(0, 0, 0), 1, material=Matte(RGBColor.Red())))
            # sphere.translate(-1, 0, -5)

            grid = Grid()
            grid.setup(triangles)

            self.add_geometry(grid)

        self.ambient_light = AmbientLight()
        self.add_point_light(PointLight(Point3(-2.5, -1.5, -1.0)))

    def add_point_light(self, light):
        sphere = Instance(Sphere(Point3(0, 0, 0), 0.1, material=Emissive()))
        sphere.translate(light.location.x, light.location.y, light.location.z)
        sphere.casts_shadows = False
        self.geometry.append(sphere)

        self.lights.append(light)

    def add_geometry(self, geometry):
        self.geometry.append(geometry)

    def render_scene(self):
        self.camera.render_scene(self)

    def ray_intersection(self, ray):
        closest_hit = TraceResult(Intersection.Miss(), None)
        for geometry in self.geometry:
            intersection = geometry.intersect(ray)
            if intersection.is_hit and intersection.is_closer(closest_hit.intersection):
                shading_record = ShadingRecord(
                    self.ambient_light,
                    self.lights,
                    intersection.material,
                    intersection.normal,
                    ray,
                    ray.extrapolate(intersection.t)
                )
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
