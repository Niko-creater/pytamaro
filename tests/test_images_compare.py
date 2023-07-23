from pytamaro import *
from pytamaro.images_compare import *


def point_graphic(x, y):
    circle = pin(center, circular_sector(10, 360, black))

    return pin(bottom_left, compose(
        pin(center, compose(circle, pin(center_right, rectangle(x, 0, white)))),
        pin(top_center, rectangle(0, y, white))))


def test_compare_pillow_images():
    background = pin(bottom_left, rectangle(500, 500, white))

    point1 = compose(point_graphic(100, 100), background)
    point2 = compose(point_graphic(200, 100), background)
    point3 = compose(point_graphic(200, 200), background)

    assert not compare_graphic(point1, point2)
    assert compare_graphic(point1, point1)

