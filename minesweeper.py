import argparse
import random

# import Zelle's Graphics module
from graphics import GraphWin, Point, Line, Text, Rectangle, GraphicsError

width = 10
height = 10
resx = 800
resy = 800
difficulty = 10

parser = argparse.ArgumentParser()
parser.add_argument(
    "-W", "--width", help="Sets the width of the playing field in units"
)
parser.add_argument(
    "-H", "--height", help="Sets the height of the playing field in units"
)
parser.add_argument("-x", "--resx", help="Sets the width of the window in pixels")
parser.add_argument("-y", "--resy", help="Sets the height of the window in pixels")
parser.add_argument(
    "-d", "--difficulty", help="Sets the difficulty, with 1 being the most difficult"
)
args = parser.parse_args()

try:
    if args.width:
        width = int(args.width)
    if args.height:
        height = int(args.height)
    if args.resx:
        resx = int(args.resx)
    if args.resy:
        resy = int(args.resy)
    if args.difficulty:
        difficulty = int(args.difficulty)
except ValueError:
    exit("Arguments must be numbers")


class Map2D:
    def __init__(self, w, h, difficulty, window):
        self.w = w
        self.h = h
        self.difficulty = difficulty
        self.window = window

        self.x_range = range(
            0, int(self.window.width + 1), int(self.window.width / self.w)
        )
        self.y_range = range(
            0, int(self.window.height + 1), int(self.window.height / self.h)
        )
        self.x_centers = []
        self.y_centers = []

        for index in range(0, len(self.x_range) - 1):
            x = self.x_range[index]
            if x > 0:
                self.line(x, 0, x, window.height)
            self.x_centers.append((self.x_range[index] + self.x_range[index + 1]) / 2)
        for index in range(0, len(self.y_range) - 1):
            y = self.y_range[index]
            if y > 0:
                self.line(0, y, window.width, y)
            self.y_centers.append((self.y_range[index] + self.y_range[index + 1]) / 2)

        allCells = {}
        for x in self.x_centers:
            allCells[x] = {}
            for y in self.y_centers:
                if random.randint(1, self.difficulty) == 1:
                    allCells[x][y] = -1
                else:
                    allCells[x][y] = 0

        for index in range(0, len(allCells.keys())):
            x = list(allCells.keys())[index]
            for jdex in range(0, len(list(allCells[x].keys()))):
                y = list(list(allCells[x].keys()))[jdex]
                count = 0
                if allCells[x][y] != -1:
                    try:
                        if (
                            allCells[list(allCells.keys())[index - 1]][
                                list(allCells[x].keys())[jdex - 1]
                            ]
                            == -1
                        ):
                            count += 1
                    except IndexError:
                        pass
                    try:
                        if allCells[x][list(allCells[x].keys())[jdex - 1]] == -1:
                            count += 1
                    except IndexError:
                        pass
                    try:
                        if (
                            allCells[list(allCells.keys())[index + 1]][
                                list(allCells[x].keys())[jdex - 1]
                            ]
                            == -1
                        ):
                            count += 1
                    except IndexError:
                        pass
                    try:
                        if allCells[list(allCells.keys())[index - 1]][y] == -1:
                            count += 1
                    except IndexError:
                        pass
                    try:
                        if allCells[list(allCells.keys())[index + 1]][y] == -1:
                            count += 1
                    except IndexError:
                        pass
                    try:
                        if (
                            allCells[list(allCells.keys())[index - 1]][
                                list(allCells[x].keys())[jdex + 1]
                            ]
                            == -1
                        ):
                            count += 1
                    except IndexError:
                        pass
                    try:
                        if allCells[x][list(allCells[x].keys())[jdex + 1]] == -1:
                            count += 1
                    except IndexError:
                        pass
                    try:
                        if (
                            allCells[list(allCells.keys())[index + 1]][
                                list(allCells[x].keys())[jdex + 1]
                            ]
                            == -1
                        ):
                            count += 1
                    except IndexError:
                        pass

                    allCells[x][y] = count

        self.allCells = allCells

    def line(self, x, y, a, b):
        _line = Line(Point(x, y), Point(a, b))
        _line.draw(self.window)

    def plot(self, x, y):
        _point = Point(x, y)
        _point.draw(self.window)

    def drawBombs(self):
        for x in self.allCells:
            for y in self.allCells[x]:
                if self.allCells[x][y] == -1:
                    star = Text(Point(x, y), "*")
                    star.setSize(36)
                    star.draw(self.window)


map = Map2D(width, height, difficulty, GraphWin("Minesweeper", resx, resy))

stop = False
hit = False
while not stop:
    try:
        click = map.window.getMouse()
    except GraphicsError:
        exit()
    if click.x in map.x_range or click.y in map.y_range:
        continue
    for column in map.x_range:
        if click.x == column:
            continue
        if click.x > column:
            hit = True
            old_col = column
            continue
        if click.x < column and hit:
            center_x = (old_col + column) / 2
            hit = False
            break

    for row in map.y_range:
        if click.y == row:
            continue
        if click.y > row:
            hit = True
            old_row = row
            continue
        if click.y < row and hit:
            center_y = (old_row + row) / 2
            hit = False
            break

    cell_value = map.allCells[center_x][center_y]
    if cell_value == -1:
        map.drawBombs()
        break

    colors = [
        "black",
        "blue",
        "green",
        "green4",
        "orange",
        "red",
        "red2",
        "red3",
        "red4",
    ]
    if cell_value == 0:
        cell_display = Rectangle(Point(old_col, old_row), Point(column, row))
        cell_display.setFill("grey")
    else:
        cell_display = Text(Point(center_x, center_y), cell_value)
        cell_display.setFill(colors[cell_value])
        cell_display.setSize(36)
    cell_display.draw(map.window)

map.window.getMouse()
map.window.close()