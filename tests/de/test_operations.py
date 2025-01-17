from pytamaro.color_names import red
from pytamaro.de.operations import (neben, grafik_hoehe, kombiniere, fixiere,
                                    grafik_breite, drehe, ueber,
                                    ueberlagere)
from pytamaro.operations import (above, beside, compose, graphic_height,
                                 graphic_width, overlay, pin, rotate)
from pytamaro.primitives import rectangle
from tests.testing_utils import HEIGHT, WIDTH
from pytamaro.de.point_names import *

g = rectangle(WIDTH, HEIGHT, red)


def test_width():
    assert graphic_width(g) == grafik_breite(g)


def test_height():
    assert graphic_height(g) == grafik_hoehe(g)


def test_rotate():
    assert rotate(45, g) == drehe(45, g)


def test_beside():
    assert beside(g, g) == neben(g, g)


def test_above():
    assert above(g, g) == ueber(g, g)


def test_overlay():
    assert overlay(g, g) == ueberlagere(g, g)


def test_compose():
    assert compose(g, g) == kombiniere(g, g)


def test_fixiere():
    assert pin(top_left, g) == fixiere(oben_links, g)
    assert pin(center, g) == fixiere(mitte, g)
    assert pin(bottom_right, g) == fixiere(unten_rechts, g)
