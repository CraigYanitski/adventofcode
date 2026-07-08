from colorama import init, Fore, Style
#import re
#from pprint import pprint

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

init(autoreset=True)

"""
Use the pattern `_9` to process with the desired date.
"""

input_test: str = \
"""7,1
   11,1
   11,7
   9,7
   9,5
   2,5
   2,3
   7,3
   """.replace('   ', '')

input_9: str = open("input_9").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    day = "Day 9"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 0
    # complete this function
    tiles = []
    x_lists = defaultdict(list)
    y_lists = defaultdict(list)
    for line in text.split():
        x, y = line.split(",")
        tiles.append([int(x), int(y)])
        x_lists[int(y)].append(int(x))
        y_lists[int(x)].append(int(y))
    x_span = []
    y_span = []
    for x, ylist in y_lists.items():
        ysort = sorted(ylist)
        for i in range(len(ysort) // 2):
            y1 = [x, ysort[2*i]]
            y2 = [x, ysort[2*i + 1]]
            y_span.append([y1, y2])
            if part == 2:
                plt.plot([y1[0], y2[0]], [y1[1], y2[1]], c="r")
    for y, xlist in x_lists.items():
        xsort = sorted(xlist)
        for i in range(len(xsort) // 2):
            x1 = [xsort[2*i], y]
            x2 = [xsort[2*i + 1], y]
            x_span.append([x1, x2])
            if part == 2:
                plt.plot([x1[0], x2[0]], [x1[1], x2[1]], c="r")
    if part == 2:
        if verbose:
            ms = 10
        else:
            ms = 3
        plt.plot(np.asarray(tiles + [tiles[0]])[:, 0], 
                 np.asarray(tiles + [tiles[0]])[:, 1],
                 marker="H",
                 ms=ms,
                 c="b")
        plt.plot(tiles[0][0], tiles[0][1], marker="x", ms=16)
    tile_map = ""
    width = 0
    height = 0
    for tile in tiles:
        width = max(width, tile[0]+2)
        height = max(height, tile[1]+2)
    if verbose:
        tile_map = create_map(width, height)
        tile_map = add_tile(tile_map, tiles)
    if part == 2:
        if verbose:
            for y, xlist in x_lists.items():
                x_tiles = []
                xsort = sorted(xlist)
                for i in range(len(xlist) // 2):
                    for x in range(1+xsort[2*i], xsort[2*i+1]):
                        x_tiles.append([x, y])
                tile_map = add_tile(tile_map, x_tiles, "X")
            for x, ylist in y_lists.items():
                y_tiles = []
                ysort = sorted(ylist)
                for i in range(len(ylist) // 2):
                    for y in range(1+ysort[2*i], ysort[2*i+1]):
                        y_tiles.append([x, y])
                tile_map = add_tile(tile_map, y_tiles, "X")
    if verbose:
        print(tile_map)
    count = 0
    square = []
    for i, tile in enumerate(tiles):
        for opp in tiles[:i]:
            valid = True
            if part == 2:
                xmin = min(tile[0], opp[0])
                xmax = max(tile[0], opp[0])
                ymin = min(tile[1], opp[1])
                ymax = max(tile[1], opp[1])
                for x1, x2 in x_span:
                    y = x1[1]
                    xl = min(x1[0], x2[0])
                    xr = max(x1[0], x2[0])
                    if (y > ymin and y < ymax):
                        if not (xr <= xmin or xl >= xmax):
                            valid = False
                            break
                if valid:
                    for y1, y2 in y_span:
                        x = y1[0]
                        yb = min(y1[1], y2[1])
                        yu = max(y1[1], y2[1])
                        if (x > xmin and x < xmax):
                            if not (yu <= ymin or yb >= ymax):
                                valid = False
                                break
                if not valid:
                    continue
            a = (abs(tile[0]-opp[0])+1) * (abs(tile[1]-opp[1])+1)
            count += 1
            if verbose:
                print(count, a, tile, opp)
            if a > total:
                square = [tile, opp]
                total = a
    if part == 2:
        plt.plot([square[0][0], square[0][0], square[1][0], square[1][0], square[0][0]], 
                 [square[0][1], square[1][1], square[1][1], square[0][1], square[0][1]], 
                 c="k")
        #plt.show()
    return total


def add_tile(_map, pos, marker="#"):
    lines = [list(p) for p in _map.split()]
    #line = list(lines[pos[1]])
    for p in pos:
        lines[p[1]][p[0]] = marker
    new_map = "\n".join(["".join(p) for p in lines])
    return new_map


def create_map(x, y):
    line = "".join(["."] * x)
    return "\n".join([line] * y)


def run_test(text, test_inputs=('', 0), part=1) -> None:
    print()
    res: int = solve(test_inputs[0], test=True, part=part, verbose=True)
    if res == test_inputs[1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        print()
        res: int = solve(text, part=part, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
        print()
    print("Part " + 'I'*part + Style.BRIGHT + f": {res}")


if __name__ == "__main__":
    run_test(input_9, (input_test, 50), part=1)
    run_test(input_9, (input_test, 24), part=2)
    
