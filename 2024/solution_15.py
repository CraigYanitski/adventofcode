from colorama import init, Fore, Style
import re
from pprint import pprint

init(autoreset=True)

input_test: str = \
"""##########
   #..O..O.O#
   #......O.#
   #.OO..O.O#
   #..O@..O.#
   #O#..O...#
   #O..O..O.#
   #.OO.O.OO#
   #....O...#
   ##########

   <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
   vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
   ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
   <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
   ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
   ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
   >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
   <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
   ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
   v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".replace('   ', '')

test1 = \
"""########
   #..O.O.#
   ##@.O..#
   #...O..#
   #.#.O..#
   #...O..#
   #......#
   ########

   <^^>>>vv<v>>v<<
""".replace('   ', '')

input_test_2: str = \
"""####################
   ##....[]....[]..[]##
   ##............[]..##
   ##..[][]....[]..[]##
   ##....[]@.....[]..##
   ##[]##....[]......##
   ##[]....[]....[]..##
   ##..[][]..[]..[][]##
   ##........[]......##
   ####################

   <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
   vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
   ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
   <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
   ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
   ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
   >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
   <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
   ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
   v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".replace('   ', '')

input_15: str = open("input_15").read()

map_: list = list()
moves: str = str()
robot: set = set()
walls: set = set()
boxes: set = set()
lboxes: set = set()
rboxes: set = set()
wall_flag: bool = False


def print_map(test=False) -> None:
    global map_
    global robot
    global walls
    global boxes
    global lboxes
    global rboxes
    if test:
        width, height = (2*len(map_[0]), len(map_))
    else:
        width, height = (len(map_[0]), len(map_))
    for y in range(height):
        for x in range(width):
            if (x, y) in walls:
                print(Fore.RED + '#', end='')
            elif (x, y) in boxes:
                print(Fore.GREEN + Style.BRIGHT + 'O', end='')
            elif ((x, y), (x+1, y)) in boxes:
                print(Fore.GREEN + Style.BRIGHT + '[]', end='')
            elif ((x-1, y), (x, y)) in boxes:
                pass#rint('[]', end='')
            elif (x, y) in robot:
                print(Fore.MAGENTA + Style.BRIGHT + '@', end='')
            else:
                print(Fore.WHITE + Style.DIM + '.', end='')
        print()
    return

def solve(text, test=False, part=1, verbose=False) -> int:
    global map_
    global moves
    del map_
    del moves
    map_str, moves = text.split('\n\n')
    map_ = list(map(lambda x: list(x), map_str.split('\n')))
    width, height = (len(map_[0]), len(map_))
    moves = moves.replace('\n', '')
    global robot
    global walls
    global boxes
    del robot
    del walls
    del boxes
    robot = set()
    walls = set()
    boxes = set()
    total: int = 0
    for x in range(width):
        for y in range(height):
            if map_[y][x] == '#' and test and part == 2:
                walls.add((2*x, y))
                walls.add((2*x+1, y))
            elif map_[y][x] == '#':
                walls.add((x, y))
            elif map_[y][x] == 'O' and part == 1:
                boxes.add((x, y))
            elif map_[y][x] == 'O' and part == 2:
                boxes.add(((2*x, y), (2*x+1, y)))
            elif map_[y][x] == '[' and part == 2:
                boxes.add(((x, y), (x+1, y)))
            elif map_[y][x] == '@' and part == 1:
                robot.add((x, y))
            elif map_[y][x] == '@' and part == 2 and test:
                robot.add((2*x, y))
            elif map_[y][x] == '@' and part == 2:
                robot.add((x, y))
    if verbose:
        print_map(test=test)
    for move in moves:
        if move == '^':
            dx, dy = 0, -1
        elif move == '<':
            dx, dy = -1, 0
        elif move == '>':
            dx, dy = 1, 0
        elif move == 'v':
            dx, dy = 0, 1
        else:
            dx, dy = 0, 0
        move_robot((dx, dy), part=part)
    #if verbose:
    print_map(test=test)
    for box in boxes:
        if part == 1:
            total += 100 * box[1] + box[0]
        else:
            total += 100 * box[0][1] + box[0][0]
    return total

def move_robot(move, part=1) -> None:
    global map_
    global robot
    global walls
    global boxes
    global wall_flag
    x, y = robot.pop()
    dx, dy = move
    nearest_boxes: list = boxes_blocking([(x, y)], move, part=part)
    if wall_flag:
        wall_flag = False
        robot.add((x, y))
        return
    elif len(nearest_boxes) == 0:
        robot.add((x+dx, y+dy))
        return
    if part == 2:
        current_boxes: list = find_boxes(nearest_boxes)
        #print(current_boxes)
    else:
        current_boxes: list = nearest_boxes
    new_boxes = []
    for box in current_boxes:
        new_boxes.append(move_box(box, move, part=part))
        boxes.remove(box)
    for box in new_boxes:
        boxes.add(box)
    robot.add((x+dx, y+dy))
    return

def robot_in_box(pos) -> bool:
    global boxes
    for box in boxes:
        if pos in box:
            return True
    return False

def box_in_box() -> bool:
    global boxes
    for box in boxes:
        for pos in boxes:
            if pos in box:
                return True
    return False

def boxes_blocking(pos, move, part=1) -> list:
    global boxes
    global walls
    global wall_flag
    dx, dy = move
    more_boxes: list = []
    more_walls: list = []
    for p in pos:
        x, y = p
        if part == 1:
            if (x+dx, y+dy) in boxes:
                more_boxes += [(x+dx, y+dy)]
        if (x+dx, y+dy) in walls:
            more_walls += [(x+dx, y+dy)]
        if dy:
            if ((x, y+dy), (x+1, y+dy)) in boxes:
                more_boxes += [(x, y+dy), (x+1, y+dy)]
            if ((x-1, y+dy), (x, y+dy)) in boxes:
                more_boxes += [(x-1, y+dy), (x, y+dy)]
            if ((x, y+dy), (x+1, y+dy)) in walls:
                more_walls += [(x, y+dy), (x+1, y+dy)]
            if ((x-1, y+dy), (x, y+dy)) in walls:
                more_walls += [(x-1, y+dy), (x, y+dy)]
        elif dx:
            if ((x+dx, y), (x+2*dx, y)) in boxes:
                more_boxes += [(x+dx, y), (x+2*dx, y)]
            if ((x+2*dx, y), (x+dx, y)) in boxes:
                more_boxes += [(x+2*dx, y), (x+dx, y)]
            if ((x+dx, y), (x+2*dx, y)) in walls:
                more_walls += [(x+dx, y), (x+2*dx, y)]
            if ((x+2*dx, y), (x+dx, y)) in walls:
                more_walls += [(x+2*dx, y), (x+dx, y)]
    more_boxes: list = list(set(more_boxes))
    more_walls: list = list(set(more_walls))
    if len(more_walls) or wall_flag:
        wall_flag = True
        return []
    if len(more_boxes) == 0:
        return more_boxes
    return more_boxes + boxes_blocking(more_boxes, move)

def find_boxes(pos):
    if len(pos) % 2:
        raise Exception("Even number of locations required for boxes - located an odd number")
    global boxes
    wide_boxes: list = []
    for p in pos:
        for _ in pos:
            if (p, _) in boxes:
                wide_boxes.append((p, _))
                break
    if 2*len(wide_boxes) == len(pos):
        pass
    else:
        raise Exception("wide boxes improperly located")
    return wide_boxes

def move_box(loc, move, part=1) -> tuple:
    #global boxes
    #boxes.remove(loc)
    dx, dy = move
    bl, br = loc
    if part == 1:
        pos: tuple = (bl+dx, br+dy)
    else:
        pos: tuple = ((bl[0]+dx, bl[1]+dy), (br[0]+dx, br[1]+dy))
    #boxes.add(pos)
    return pos


def run_test(text, test=(False,), test_inputs=[('', 0)], part=1) -> None:
    res: int = solve(test_inputs[0][0], test=test[0], part=part, verbose=True)
    print()
    if res == test_inputs[0][1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        if len(test_inputs) > 1:
            res: int = solve(test_inputs[1][0], test=test[1], part=part, verbose=True)
            if res == test_inputs[1][1]:
                print(Fore.GREEN + "All tests passed!!")
                res: int = solve(text, test=test[-1], part=part, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
    print()
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_15, test=(False, False), test_inputs=[(test1, 2028), (input_test, 10092)], part=1)
    print('='*10)
    run_test(input_15, test=(False, True), test_inputs=[(input_test_2, 9021), (input_test, 9021)], part=2)
    
