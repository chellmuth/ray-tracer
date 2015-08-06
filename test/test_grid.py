from geometry import Sphere as S
from grid import Grid as G
from grid import FixedCellStrategy as CS
from material import Material as M
from point import Point3 as P
from ray import Ray as R
from vector import Vector3 as V

def test_grid_basic():
    grid = G(CS(1))
    sphere = S(P(0, 0, 0), 1, M())
    grid.setup([sphere])

    assert grid.cells == [[sphere]]

def test_grid_spans_multiple_cells():
    grid = G(CS(2))
    sphere = S(P(0, 0, 0), 1, M())
    grid.setup([sphere])

    assert grid.cells == [[sphere] for _ in range(8)]

def test_grid_contains_multiple_objects():
    grid = G(CS(1))
    sphere1 = S(P(0, 0, 0), 1, M())
    sphere2 = S(P(0, 0, 0), 1, M())
    grid.setup([sphere1, sphere2])

    assert grid.cells == [[sphere1, sphere2]]

def test_objects_in_different_cells():
    grid = G(CS(2))
    sphere1 = S(P(-1, 1, 1), 0.99, M())
    sphere2 = S(P(1, 1, 1), 0.99, M())
    grid.setup([sphere1, sphere2])

    cells = [
        # (x: 0, y: 0, z: 0), (x: 1, y: 0, z: 0)
        [sphere1],            [sphere2],
        # (x: 0, y: 1, z: 0), (x: 1, y: 1, z: 0)
        [sphere1],            [sphere2],
        # (x: 0, y: 0, z: 1), (x: 1, y: 0, z: 1)
        [sphere1],            [sphere2],
        # (x: 0, y: 1, z: 1), (x: 1, y: 1, z: 1)
        [sphere1],            [sphere2]
    ]
    assert grid.cells == cells

def test_different_sized_objects():
    grid = G(CS(2))
    sphere1 = S(P(-1, -1, 1), 0.99, M())
    sphere2 = S(P(1.5, 1.5, -1.5), 0.49, M())
    grid.setup([sphere1, sphere2])


    # [[], [], [], [C: ((1.500000, 1.500000, -1.500000)), r: 0.49], [C: ((-1.000000, -1.000000, 1.000000)), r: 0.99], [], [], []]
    cells = [
        # (x: 0, y: 0, z: 0), (x: 1, y: 0, z: 0)
        [],                   [],
        # (x: 0, y: 1, z: 0), (x: 1, y: 1, z: 0)
        [],                   [sphere2],
        # (x: 0, y: 0, z: 1), (x: 1, y: 0, z: 1)
        [sphere1],            [],
        # (x: 0, y: 1, z: 1), (x: 1, y: 1, z: 1)
        [],                   []
    ]
    assert grid.cells == cells

def test_hit_basic():
    grid = G(CS(10))
    sphere = S(P(2, 2, 2), 1, M())
    grid.setup([sphere])

    assert grid.hit(R(P(0, 0, 0), V(1, 1, 1))).is_hit
