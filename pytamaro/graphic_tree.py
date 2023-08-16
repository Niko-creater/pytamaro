import sys
from abc import ABC
from dataclasses import dataclass

from pytamaro import Color




@dataclass
class GraphicTree(ABC):
    root: str
    left_node: None
    right_node: None


class OperationNode(GraphicTree):
    def __init__(self, operator: str):
        self.root = operator


class PinNode(OperationNode):
    def __init__(self, point: str, graphic: GraphicTree):
        self.point = point
        self.graphic = graphic
        self.left_node = point
        self.right_node = graphic
        super().__init__("pin")


class ComposeNode(OperationNode):
    def __init__(self, foreground_graphic: GraphicTree, background_graphic: GraphicTree):
        self.foreground_graphic = foreground_graphic
        self.background_graphic = background_graphic
        self.left_node = foreground_graphic
        self.right_node = background_graphic
        super().__init__("compose")


class RotateNode(OperationNode):
    def __init__(self, angle: float, graphic: GraphicTree):
        self.angle = -angle
        self.graphic = graphic
        self.left_node = -angle
        self.right_node = graphic
        super().__init__("rotate")


class PrimitiveNode(GraphicTree):
    def __init__(self, operand: str, data: str, col: str):
        self.root = operand
        self.data = data
        self.col = col



class RectangleNode(PrimitiveNode):
    def __init__(self, width: float, height: float, color: str):
        self.width = width
        self.height = height
        self.color = color
        data = "w:" + str(width) + ",h:" + str(height)
        self.left_node = data
        self.right_node = color
        super().__init__("rectangle", data, color)


class TriangleNode(PrimitiveNode):
    def __init__(self, side1: float, side2: float, angle: float, color: str):
        self.side1 = side1
        self.side2 = side2
        self.angle = angle
        self.color = color
        data = "s1:" + str(side1) + ",s2:" + str(side2) + ",a:" + str(angle)
        self.left_node = data
        self.right_node = color
        super().__init__("triangle", data, color)


class EllipseNode(PrimitiveNode):
    def __init__(self, width: float, height: float, color: str):
        self.width = width
        self.height = height
        self.color = color
        data = "w:" + str(width) + ",h:" + str(height)
        self.left_node = data
        self.right_node = color
        super().__init__("ellipse", data, color)


class CircularSectorNode(PrimitiveNode):
    def __init__(self, radius: float, angle: float, color: str):
        self.radius = radius
        self.color = color
        self.angle = angle
        data = "r:" + str(radius) + ",a:" + str(angle)
        self.left_node = data
        self.right_node = color
        super().__init__("circularSector", data, color)


class TextNode(PrimitiveNode):
    def __init__(self, content: str, font: str, points: float, color: str):
        self.content = content
        self.font = font
        self.points: points
        self.color = color
        data = "c:" + content + ",f:" + font + ",p:" + str(points)
        self.left_node = data
        self.right_node = color
        super().__init__("text", data, color)


class EmptyNode(PrimitiveNode):
    def __init__(self):
        super().__init__("empty", " ", " ")
        self.left_node = "000"
        self.right_node = "none"


class Canvas:
    def __init__(self, width):
        self.line_width = width
        self.canvas = []

    def put_char(self, x, y, c):
        if x < self.line_width:
            pos = y * self.line_width + x
            l = len(self.canvas)
            if pos < l:
                self.canvas[pos] = c
            else:
                self.canvas[l:] = [' '] * (pos - l)
                self.canvas.append(c)

    def print_out(self):
        i = 0
        sp = 0
        for c in self.canvas:
            if c != ' ':
                sys.stdout.write(' ' * sp)
                sys.stdout.write(c)
                sp = 0
            else:
                sp += 1
            i = i + 1
            if i % self.line_width == 0:
                sys.stdout.write('\n')
                sp = 0
        if i % self.line_width != 0:
            sys.stdout.write('\n')


def print_binary_tree_r(t, x: int, y: int, canvas: Canvas):
    max_y = y
    if isinstance(t, GraphicTree):
        x, max_y, lx, rx = print_binary_tree_r(t.left_node, x, y + 2, canvas)
        x = x + 1
        for i in range(rx, x):
            canvas.put_char(i, y + 1, '/')

    middle_l = x
    if isinstance(t, GraphicTree):
        for c in str(t.root):
            canvas.put_char(x, y, c)
            x = x + 1
    elif isinstance(t, str):
        for c in t:
            canvas.put_char(x, y, c)
            x = x + 1
    middle_r = x

    if isinstance(t, GraphicTree):
        canvas.put_char(x, y + 1, '\\')
        x = x + 1
        x0, max_y2, lx, rx = print_binary_tree_r(t.right_node, x, y + 2, canvas)
        if max_y2 > max_y:
            max_y = max_y2
        for i in range(x, lx):
            canvas.put_char(i, y + 1, '\\')
        x = x0

    return x, max_y, middle_l, middle_r


def print_tree(t):
    print_tree_w(t, 30000)


def print_tree_w(t, width):
    canvas = Canvas(width)
    print_binary_tree_r(t, 0, 0, canvas)
    canvas.print_out()
