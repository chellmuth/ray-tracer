import itertools

from util import clamp

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

class Grid(object):
    def __init__(self, cell_strategy):
        self.cell_strategy = cell_strategy

    def setup(self, objects):
        self.cells = self._calculate_cells(objects)

    def _calculate_cells(self, objects):
        bbox = self._calculate_bounds(objects)

        n_x, n_y, n_z = self.cell_strategy.n(bbox, objects)
        n = n_x * n_y * n_z
        cells = [ [] for _ in range(n) ]

        for obj in objects:
            obj_bbox = obj.get_bbox()

            x_range = range(
                int(clamp((obj_bbox.p0.x - bbox.p0.x) * n_x / (bbox.p1.x - bbox.p0.x), 0, n_x)),
                int(clamp((obj_bbox.p1.x - bbox.p0.x) * n_x / (bbox.p1.x - bbox.p0.x), 0, n_x) + 1)
            )

            y_range = range(
                int(clamp((obj_bbox.p0.y - bbox.p0.y) * n_y / (bbox.p1.y - bbox.p0.y), 0, n_y)),
                int(clamp((obj_bbox.p1.y - bbox.p0.y) * n_y / (bbox.p1.y - bbox.p0.y), 0, n_y) + 1)
            )

            z_range = range(
                int(clamp((obj_bbox.p0.z - bbox.p0.z) * n_z / (bbox.p1.z - bbox.p0.z), 0, n_z)),
                int(clamp((obj_bbox.p1.z - bbox.p0.z) * n_z / (bbox.p1.z - bbox.p0.z), 0, n_z) + 1)
            )

            for x, y, z in itertools.product(x_range, y_range, z_range):
                index = x + n_x * y + n_x * n_y * z
                cells[index].append(obj)

        return cells

    def _calculate_bounds(self, objects):
        if len(objects) == 0: raise ValueError
        bbox = objects[0].get_bbox()
        for obj in objects[1:]:
            bbox = bbox.union(obj.get_bbox())

        return bbox.grow_epsilon()
