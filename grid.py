import collections
import itertools

from util import clamp
from vector import Vector3

from geometry import Intersection
from material import Normal

epsilon = 0.001

# Ray Tracing From the Ground Up, p 448
multiplier = 2

class CellStrategy(object):
    def n(self, bbox, objects):
        raise Error

class FixedCellStrategy(CellStrategy):
    def __init__(self, axis_count):
        self.axis_count = axis_count

    def n(self, bbox, objects):
        return (self.axis_count, self.axis_count, self.axis_count)

class MultiplierCellStrategy(CellStrategy):
    def n(self, bbox, objects):
        extent_x = bbox.p1.x - bbox.p0.x
        extent_y = bbox.p1.y - bbox.p0.y
        extent_z = bbox.p1.z - bbox.p0.z

        s = pow(extent_x * extent_y * extent_z / len(objects), 1/3.)
        n_x = int(multiplier * extent_x / s + 1)
        n_y = int(multiplier * extent_y / s + 1)
        n_z = int(multiplier * extent_z / s + 1)

        return (n_x, n_y, n_z)

Interval = collections.namedtuple("Interval", ["min", "max"])

class Grid(object):
    def __init__(self, cell_strategy=None):
        self.cell_strategy = cell_strategy or MultiplierCellStrategy()

    def setup(self, objects):
        self.bbox = _calculate_bounds(objects)
        self.nx, self.ny, self.nz = self.cell_strategy.n(self.bbox, objects)
        self.n = Vector3(self.nx, self.ny, self.nz)
        self.cells = self._calculate_cells(objects)

    @property
    def material(self):
        return Normal()

    def intersect(self, ray):
        return self.hit(ray)

    def hit(self, ray):
        bbox = self.bbox
        nx, ny, nz = self.nx, self.ny, self.nz

        if not bbox.is_hit(ray):
            return Intersection.Miss()

        # Get first and last intersections on each axis
        tx, ty, tz = _calculate_t_interval(bbox, ray)
        t_min = Vector3(tx.min, ty.min, tz.min)
        t_max = Vector3(tx.max, ty.max, tz.max)

        # Get first and last intersections on the ray
        t0 = min(tx.min, ty.min, tz.min)
        t1 = max(tx.max, ty.max, tz.max)

        # Calculate initial cell
        cell = None
        bbox_length = bbox.p1 - bbox.p0
        if bbox.is_inside(ray.origin):
            cell = Vector3(
                int(clamp(nx * (ray.origin.x - bbox.p0.x) / bbox_length.x, 0, nx - 1)),
                int(clamp(ny * (ray.origin.y - bbox.p0.y) / bbox_length.y, 0, ny - 1)),
                int(clamp(nz * (ray.origin.z - bbox.p0.z) / bbox_length.z, 0, nz - 1))
            )
        else:
            hit = ray.extrapolate(t0)
            cell = Vector3(
                int(clamp(nx * (hit.x - bbox.p0.x) / bbox_length.x, 0, nx - 1)),
                int(clamp(ny * (hit.y - bbox.p0.y) / bbox_length.y, 0, ny - 1)),
                int(clamp(nz * (hit.z - bbox.p0.z) / bbox_length.z, 0, nz - 1))
            )

        # Parameter deltas to increment cell
        t_delta = Vector3(
            (tx.max - tx.min) / self.nx,
            (ty.max - ty.min) / self.ny,
            (tz.max - tz.min) / self.nz
        )

        # t_next will get updated during traversal,
        # t_step and t_stop are const
        t_next = Vector3(None, None, None)
        cell_step = Vector3(None, None, None)
        cell_stop = Vector3(None, None, None)
        for axis in range(3):
            if t_delta[axis] > 0:
                t_next[axis] = t_delta[axis] * (cell[axis] + 1) + t_min[axis]
                cell_step[axis] = +1
                cell_stop[axis] = self.n[axis]
            elif t_delta[axis] == 0.0:
                tx_next[axis] = float("inf")
                cell_step[axis] = -1
                cell_stop[axis] = -1
            else:
                t_next[axis] = t_delta[axis] * (self.n[axis] - cell[axis]) + t_min[axis]
                cell_step[axis] = -1
                cell_stop[axis] = -1

        # Traversal
        while True:
            objs = self.cells[cell.x + self.nx * cell.y + self.nx * self.ny * cell.z]
            for axis in range(3):
                if t_next[axis] <= min(t_next[(axis+1) % 3], t_next[(axis+2) % 3]):
                    for obj in objs:
                        intersection = obj.intersect(ray)
                        if intersection.is_hit and intersection.t < t_next[axis]:
                            return intersection
                    t_next[axis] += t_delta[axis]
                    cell[axis] += cell_step[axis]
                    if cell[axis] == cell_stop[axis]:
                        return Intersection.Miss()


    def _calculate_cells(self, objects):
        bbox = self.bbox
        nx, ny, nz = self.nx, self.ny, self.nz

        n = nx * ny * nz
        cells = [ [] for _ in range(n) ]

        for obj in objects:
            obj_bbox = obj.get_bbox()

            x_range = range(
                int(clamp((obj_bbox.p0.x - bbox.p0.x) * nx / (bbox.p1.x - bbox.p0.x), 0, nx)),
                int(clamp((obj_bbox.p1.x - bbox.p0.x) * nx / (bbox.p1.x - bbox.p0.x), 0, nx) + 1)
            )

            y_range = range(
                int(clamp((obj_bbox.p0.y - bbox.p0.y) * ny / (bbox.p1.y - bbox.p0.y), 0, ny)),
                int(clamp((obj_bbox.p1.y - bbox.p0.y) * ny / (bbox.p1.y - bbox.p0.y), 0, ny) + 1)
            )

            z_range = range(
                int(clamp((obj_bbox.p0.z - bbox.p0.z) * nz / (bbox.p1.z - bbox.p0.z), 0, nz)),
                int(clamp((obj_bbox.p1.z - bbox.p0.z) * nz / (bbox.p1.z - bbox.p0.z), 0, nz) + 1)
            )

            for x, y, z in itertools.product(x_range, y_range, z_range):
                index = x + nx * y + nx * ny * z
                cells[index].append(obj)

        return cells

def _calculate_bounds(objects):
    if len(objects) == 0: raise ValueError
    bbox = objects[0].get_bbox()
    for obj in objects[1:]:
        bbox = bbox.union(obj.get_bbox())

    return bbox.grow_epsilon()


def _calculate_t_interval(bbox, ray):
    direction = ray.direction

    tx = ty = tz = None
    tx = Interval(
        min=(bbox.p0.x - ray.origin.x) / direction.x,
        max=(bbox.p1.x - ray.origin.x) / direction.x
    )
    if direction.x < 0:
        tx = Interval(tx.max, tx.min)

    ty = Interval(
        min=(bbox.p0.y - ray.origin.y) / direction.y,
        max=(bbox.p1.y - ray.origin.y) / direction.y
    )
    if direction.y < 0:
        ty = Interval(ty.max, ty.min)

    tz = Interval(
        min=(bbox.p0.z - ray.origin.z) / direction.z,
        max=(bbox.p1.z - ray.origin.z) / direction.z
    )
    if direction.x < 0:
        tz = Interval(tz.max, tz.min)

    return tx, ty, tz
