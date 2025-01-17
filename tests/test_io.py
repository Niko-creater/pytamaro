from tempfile import NamedTemporaryFile

from PIL import Image as ImageMod
from pytamaro.color_names import blue, red
from pytamaro.io import save_animation, save_graphic, show_animation, show_graphic
from pytamaro.primitives import empty_graphic, rectangle
from pytest import raises
from pytamaro.operations import beside

from tests.testing_utils import HEIGHT, WIDTH, assert_SVG_file_width_height


def test_show_graphic():
    # Implicitly assert that it does not throw
    show_graphic(rectangle(WIDTH, HEIGHT, red))


def test_show_animation():
    # Implicitly assert that it does not throw
    show_animation([rectangle(WIDTH, HEIGHT, red)])


def test_show_empty_graphic(capfd):
    # Implicitly assert that it does not throw
    show_graphic(empty_graphic())
    out, _ = capfd.readouterr()
    assert "0x0" in out


def test_show_debug_graphic():
    # Implicitly assert that it does not throw
    show_graphic(rectangle(WIDTH, HEIGHT, red), debug=True)


def test_gif_no_ext():
    with raises(ValueError, match=".gif"):
        save_animation("foo", [rectangle(WIDTH, HEIGHT, red)])


def test_empty_save_animation():
    with raises(ValueError):
        save_animation("foo.gif", [])


def test_show_wrong_type():
    with raises(TypeError, match="NoneType"):
        show_graphic(None)  # type: ignore


def test_save_animation():
    r1 = rectangle(WIDTH, HEIGHT, red)
    r2 = rectangle(WIDTH, HEIGHT, blue)
    with NamedTemporaryFile() as f:
        filename = f"{f.name}.gif"
        save_animation(filename, [r1, r2])
        gif = ImageMod.open(filename)
        assert gif.n_frames == 2


def test_save_graphic_PNG():
    r = rectangle(WIDTH, HEIGHT, red)
    with NamedTemporaryFile() as f:
        filename = f"{f.name}.png"
        save_graphic(filename, r)
        graphic = ImageMod.open(filename)
        assert graphic.size == (WIDTH, HEIGHT)


def test_save_empty_graphic_SVG():
    with NamedTemporaryFile() as f:
        filename = f"{f.name}.svg"
        save_graphic(filename, empty_graphic())
        assert_SVG_file_width_height(filename, 0, 0)


def test_save_graphic_SVG():
    r = rectangle(WIDTH, HEIGHT, red)
    with NamedTemporaryFile() as f:
        filename = f"{f.name}.svg"
        save_graphic(filename, r)
        assert_SVG_file_width_height(filename, WIDTH, HEIGHT)


def test_save_graphic_wrong_no_ext():
    r = rectangle(WIDTH, HEIGHT, red)
    with NamedTemporaryFile() as f:
        filename = f"{f.name}"
        with raises(ValueError, match="png|svg"):
            save_graphic(filename, r)


def test_save_empty_graphic_as_PNG(capfd):
    # Implicitly assert that it does not throw
    with NamedTemporaryFile() as f:
        save_graphic(f"{f.name}.png", empty_graphic())
        out, _ = capfd.readouterr()
        assert "0x0" in out


DATA_URI_11RED_RECT = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/iZk9HQAAAABJRU5ErkJggg=="
DATA_URI_11RED_RECT_GIF = "data:image/gif;base64,R0lGODlhAQABAIEAAP8AAAAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh+QQBBAABACwAAAAAAQABAAAIBAABBAQAOw=="
PREFIX = "@@@PYTAMARO_DATA_URI_BEGIN@@@"
SUFFIX = "@@@PYTAMARO_DATA_URI_END@@@"


def test_data_uri_output(capfd):
    import os

    VAR = "PYTAMARO_OUTPUT_DATA_URI"
    os.environ[VAR] = "True"
    r = rectangle(1, 1, red)
    show_graphic(r)
    out, _ = capfd.readouterr()
    assert (
        out == f"{PREFIX}{DATA_URI_11RED_RECT}{SUFFIX}"
    )
    del os.environ[VAR]


def test_multiple_data_uri_mixed_output(capfd):
    import os

    VAR = "PYTAMARO_OUTPUT_DATA_URI"
    os.environ[VAR] = "True"
    r = rectangle(1, 1, red)
    print(42)
    show_graphic(r)
    print(42)
    show_graphic(r)
    print(42)
    out, _ = capfd.readouterr()
    assert (
        out == f"42\n{PREFIX}{DATA_URI_11RED_RECT}{SUFFIX}42\n{PREFIX}{DATA_URI_11RED_RECT}{SUFFIX}42\n"
    )
    del os.environ[VAR]


def test_data_uri_gif_output(capfd):
    import os

    VAR = "PYTAMARO_OUTPUT_DATA_URI"
    os.environ[VAR] = "True"
    r = rectangle(1, 1, red)
    show_animation([r])
    out, _ = capfd.readouterr()
    assert (
        out
        == f"{PREFIX}{DATA_URI_11RED_RECT_GIF}{SUFFIX}"
    )
    del os.environ[VAR]


def test_show_deeply_nested_graphic():
    element = rectangle(WIDTH, HEIGHT, red)
    from functools import reduce
    graphic = reduce(beside, [element] * 1000, empty_graphic())
    # Implicitly assert that it does not throw
    show_graphic(graphic)
