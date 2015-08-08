from color import RGBColor
from point import Point3
from ray import Ray
from vector import Vector3

class Camera(object):
    def __init__(self):
        self.eye = Point3(0, 30, 340)
        self.look_at = Point3(3, 30, 0)
        self.up = Vector3(0, 1, 0)
        self.view_distance = 400

        self.u, self.v, self.w = self._compute_uvw()

    def _compute_uvw(self):
        w = (self.eye - self.look_at).normalized()
        u = self.up.cross(w).normalized()
        v = w.cross(u)

        return (u, v, w)

    def render_scene(self, world):
        hres = world.view_plane.hres
        vres = world.view_plane.vres
        pixel_size = world.view_plane.pixel_size
        for row in range(vres):
            for col in range(hres):
                color = RGBColor.Black()
                samples = world.sampler.generate_samples()
                for sample in samples:
                    x = pixel_size * (col - 0.5 * hres + sample.x)
                    y = pixel_size * (row - 0.5 * vres + sample.y)

                    ray = self._generate_ray(x, y)
                    color += world.tracer.trace_ray(ray)

                color /= len(samples)

                world.display_pixel(vres - row - 1, col, color)

    def _generate_ray(self, x, y):
        direction = self.u.mult(x) + self.v.mult(y) - self.w.mult(self.view_distance)
        return Ray(self.eye, direction.normalized())
