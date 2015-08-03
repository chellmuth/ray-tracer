from bbox import BoundingBox as BB
from point import Point3 as P
from ray import Ray as R
from vector import Vector3 as V

def test_bbox_basic_hit():
    bbox = BB(P(1, 1, 1), P(2, 2, 2))
    assert bbox.is_hit(R(P(0, 0, 0), V(1, 1, 1)))

def test_bbox_basic_miss():
    bbox = BB(P(1, 1, 1), P(2, 2, 2))
    assert not bbox.is_hit(R(P(0, 0, 0), V(-1, 1, 1)))
    assert not bbox.is_hit(R(P(0, 0, 0), V(1, -1, 1)))
    assert not bbox.is_hit(R(P(0, 0, 0), V(1, 1, -1)))

def test_start_inside_box():
    bbox = BB(P(0, 0, 0), P(1, 1, 1))
    assert bbox.is_hit(R(P(0.5, 0.5, 0.5), V(1, 1, 1)))

def test_hit_box_behind_ray():
    bbox = BB(P(1, 1, 1), P(2, 2, 2))
    assert not bbox.is_hit(R(P(0, 0, 0), V(-1, -1, -1)))

def test_reject_ray_starting_on_edge_and_moving_away():
    # t0 < epsilon
    bbox = BB(P(0, 0, 0), P(1, 1, 1))
    assert not bbox.is_hit(R(P(0, 0, 0), V(-1, -1, -1)))

def test_ray_rides_edge_of_bbox():
    bbox = BB(P(0, 0, 0), P(1, 1, 1))
    assert bbox.is_hit(R(P(0, 0, 0), V(1, 0, 0)))

def test_ray_parallel_to_bbox():
    bbox = BB(P(1, 1, 1), P(2, 2, 2))
    assert not bbox.is_hit(R(P(0, 0, 0), V(1, 0, 0)))
    assert not bbox.is_hit(R(P(0, 0, 0), V(-1, 0, 0)))
