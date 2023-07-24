from pytamaro import *
from pytamaro.images_compare import *
from unittest import TestCase


def point_graphic(x, y):
    background = pin(bottom_left, rectangle(500, 500, white))
    circle = pin(center, circular_sector(10, 360, black))

    return compose(pin(bottom_left, compose(
        pin(center, compose(circle, pin(center_right, rectangle(x, 0, white)))),
        pin(top_center, rectangle(0, y, white)))), background)


def test_compare_pillow_images():
    point1 = point_graphic(100, 100)
    point2 = point_graphic(200, 100)
    point3 = point_graphic(200, 200)

    assert not compare_graphic(point1, point2)
    assert compare_graphic(point1, point1)
    # TestCase.assertRaises(SystemExit, compare_graphic(rectangle(200, 200, red), rectangle(100, 100, red)))


def test_compare_images():
    test_graphic_png = "../examples/test_graphic.png"
    test_graphic1_png = "../examples/test_graphic1.png"
    test_graphic2_png = "../examples/test_graphic2.png"
    test_graphic_svg = "../examples/red.svg"
    test_graphic1_svg = "../examples/red_with_black_dot.svg"

    assert compare_images(test_graphic_png, test_graphic1_png)
    assert not compare_images(test_graphic_png, test_graphic2_png)
    assert compare_images(test_graphic_svg, test_graphic_svg)
    assert not compare_images(test_graphic_svg, test_graphic1_svg)


def test_compare_animation():
    assert compare_animation("../examples/test_animation.gif", "../examples/test_animation.gif")
    assert not compare_animation("../examples/test_animation.gif", "../examples/test_animation1.gif")
