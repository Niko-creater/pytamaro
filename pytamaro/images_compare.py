import io
import sys
import xml.etree.ElementTree as ET
from typing import Tuple

import cairosvg
import numpy as np
from PIL import Image as PILImageMod
from pytamaro.graphic import Graphic
from PIL.Image import Image as PILImage
from pytamaro.io import graphic_to_pillow_image


def validate_file_contents(file1: str, file2: str) -> bool:
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        contents1 = f1.read()
        contents2 = f2.read()
    return contents1 == contents2


def compare_pillow_images(pic1: PILImage, pic2: PILImage) -> bool:
    """

    :param pic1: the given Pillow image
    :param pic2: the authenticated Pillow image
    :return: True if two images are exactly same, otherwise return False and display
    an image which indicate the different part of the two images

    """
    pic1_arr = np.array(pic1)
    pic2_arr = np.array(pic2)

    pic1_height = len(pic1_arr)
    pic1_width = len(pic1_arr[0])

    pic2_height = len(pic2_arr)
    pic2_width = len(pic2_arr[0])

    if pic1_height != pic2_height or pic1_width != pic2_width:
        sys.exit("Images are incomparable: Different images size")
    bit_map = np.zeros((pic1_height, pic1_width, 4), dtype="uint8")
    count = 0

    for i in range(pic1_height):
        for j in range(pic1_width):
            if (pic1_arr[i][j] == pic2_arr[i][j]).all():
                bit_map[i][j] = np.array([255, 255, 255, 255], dtype="uint8")
            else:
                bit_map[i][j] = np.array([255, 0, 0, 255], dtype="uint8")
                count += 1
    error = count / (pic1_width * pic1_height)
    if error != 0:
        print(f"The difference between two pictures is {error * 100:.3f}%")
        PILImageMod.fromarray(bit_map).show()
        return False
    else:
        print("Two images are same")
        return True


def compare_graphic(graphic1: Graphic, graphic2: Graphic) -> bool:
    """

    :param graphic1: the given Graphic
    :param graphic2: the authenticated Graphic
    :return: True if two Graphics are exactly same, otherwise return False and display
    an image which indicate the different part of the two Graphics

    """
    img1 = graphic_to_pillow_image(graphic1)
    img2 = graphic_to_pillow_image(graphic2)

    result = compare_pillow_images(img1, img2)

    return result


def read_svg(file1: str, file2: str) -> Tuple[PILImage, PILImage]:
    """
    :param file1: the given svg file
    :param file2: the authenticated svg file
    :return: PIL Image version file1 and PIL Image version file2

    """
    # read the svg image in XML and parse it
    pic1 = ET.parse(file1)
    pic2 = ET.parse(file2)

    # read the images' attributes
    pic1_attribs = pic1.getroot().attrib
    pic2_attribs = pic2.getroot().attrib

    width = 0
    height = 0

    if 'width' and 'height' in pic2_attribs:
        if 'width' and 'height' in pic1_attribs:
            if pic1_attribs['width'] != pic2_attribs['width'] or pic1_attribs['height'] != pic2_attribs['height']:
                sys.exit("Images are incomparable: different size")
            else:
                width, height = int(pic2_attribs['width']), int(pic2_attribs['height'])
        else:
            sys.exit("Images are incomparable: the given svg image does not have the size")
    else:
        # since there is no assigned size for authenticated svg file, a random size id picked
        width, height = 500, 500

    pic1_bytes = cairosvg.svg2png(url=file1, output_width=width, output_height=height)
    pic2_bytes = cairosvg.svg2png(url=file2, output_width=width, output_height=height)

    pic1_image = PILImageMod.open(io.BytesIO(pic1_bytes))
    pic2_image = PILImageMod.open(io.BytesIO(pic2_bytes))

    return pic2_image, pic1_image


def read_png(file1: str, file2: str) -> Tuple[PILImage, PILImage]:
    """

    :param file1: the given png file
    :param file2: the authenticated png file
    :return: PIL Image version file1 and PIL Image version file2

    """
    pic1, pic2 = PILImageMod.open(file1), PILImageMod.open(file2)

    if pic1.size != pic2.size:
        sys.exit("Images are incomparable: different size")

    return pic1, pic2


def compare_images(file1: str, file2: str) -> bool:
    """
    :param file1: the given image file
    :param file2: the authenticated image file
    :return: True if two images are exactly same, otherwise return False and display
    an image which indicate the different part of the two images

    """
    pic1 = None
    pic2 = None

    if file1.endswith(".svg") and file2.endswith(".svg"):
        pic1, pic2 = read_svg(file1, file2)
    elif file1.endswith(".png") and file2.endswith(".png"):
        pic1, pic2 = read_png(file1, file2)
    else:
        sys.exit("Images files are not supported")

    result = compare_pillow_images(pic1, pic2)

    return result


def compare_animation(file1: str, file2: str) -> bool:
    """
    :param file1: the given gif file
    :param file2: the authenticated gif file
    :return: True if two gif animation are exactly same, otherwise return False and display
    the sequence numbers of different frames

    """
    gif1 = None
    gif2 = None

    if file1.endswith(".gif") and file2.endswith(".gif"):
        gif1, gif2 = PILImageMod.open(file1), PILImageMod.open(file2)
    else:
        sys.exit("The type of files are not supported")

    if gif1.n_frames != gif2.n_frames:
        sys.exit("Two gif files are incomparable: different frames number")

    if gif1.size != gif2.size:
        sys.exit("Two gif files are incomparable: different frame size")

    result = []
    width = gif1.size[0]
    height = gif1.size[1]

    for i in range(gif1.n_frames):
        gif1.seek(i)
        gif2.seek(i)

        gif1_arr = np.array(gif1)
        gif2_arr = np.array(gif2)

        for j in range(width):
            for k in range(height):
                if not (gif1_arr[j][k] == gif2_arr[j][k]).all():
                    if len(result) == 0 or result[-1] != i:
                        result.append(i)

    if result:
        print(result)
        return False
    else:
        print("Two animations are same")
        return True


