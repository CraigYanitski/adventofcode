from colorama import init, Fore, Style
from pprint import pprint
from copy import deepcopy

init(autoreset=True)

input_test1: list = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".split()

input_6: list = open("input_6").readlines()


def print_grid(grid: list):
    for line in grid:
        #print(''.join(line))
        for c in line:
            if c == '.':
                print(Style.DIM+Fore.WHITE+c, end='')
            elif c == '#':
                print(Style.BRIGHT+Fore.BLUE+c, end='')
            elif c == 'X':
                print(Style.DIM+Fore.RED+c, end='')
            elif c == 'O':
                print(Style.BRIGHT+Fore.MAGENTA+c, end='')
        print()

def grid_to_text(grid: list):
    return '\n'.join([''.join([l for l in line]) for line in grid])

def guard_path(text: list, verbose=False, max_steps=10000) -> tuple:
    grid: list = [[c for c in line] for line in text]
    height: int = len(grid)
    width: int = len(grid[0])
    new_grid: list = [['.' for w in range(width)] for h in range(height)]
    chars: str = '^>v<'
    guard_loc: list = [None, None]
    guard_char = None
    on_duty: bool = True
    dist_locs: int = 1
    steps = 0
    if verbose:
        print_grid(grid)
        print()
    for c in chars:
        for i, line in enumerate(grid):
            if not c in line:
                continue
            guard_char = c
            guard_loc = [i, line.index(c)]
    new_grid[guard_loc[0]][guard_loc[1]] = 'X'
    if verbose:
        print(guard_loc)
        print_grid(new_grid)
        print()
    while on_duty:
        if steps > max_steps:
            return 0, new_grid
        if guard_char == '^':
            dh, dw = -1, 0
            if guard_loc[0] == 0:
                on_duty = False
            elif grid[guard_loc[0]+dh][guard_loc[1]+dw] == '#':
                guard_char = '>'
                new_grid[guard_loc[0]+dh][guard_loc[1]+dw] = '#'
            else:
                guard_loc = [guard_loc[0]+dh, guard_loc[1]+dw]
                if new_grid[guard_loc[0]][guard_loc[1]] != 'X':
                    new_grid[guard_loc[0]][guard_loc[1]] = 'X'
                    dist_locs += 1
        elif guard_char== '>':
            dh, dw = 0, 1
            if guard_loc[1] == width-1:
                on_duty = False
            elif grid[guard_loc[0]+dh][guard_loc[1]+dw] == '#':
                guard_char = 'v'
                new_grid[guard_loc[0]+dh][guard_loc[1]+dw] = '#'
            else:
                guard_loc = [guard_loc[0]+dh, guard_loc[1]+dw]
                if new_grid[guard_loc[0]][guard_loc[1]] != 'X':
                    new_grid[guard_loc[0]][guard_loc[1]] = 'X'
                    dist_locs += 1
        elif guard_char== 'v':
            dh, dw = 1, 0
            if guard_loc[0] == height-1:
                on_duty = False
            elif grid[guard_loc[0]+dh][guard_loc[1]+dw] == '#':
                guard_char = '<'
                new_grid[guard_loc[0]+dh][guard_loc[1]+dw] = '#'
            else:
                guard_loc = [guard_loc[0]+dh, guard_loc[1]+dw]
                if new_grid[guard_loc[0]][guard_loc[1]] != 'X':
                    new_grid[guard_loc[0]][guard_loc[1]] = 'X'
                    dist_locs += 1
        elif guard_char== '<':
            dh, dw = 0, -1
            if guard_loc[1] == 0:
                on_duty = False
            elif grid[guard_loc[0]+dh][guard_loc[1]+dw] == '#':
                guard_char = '^'
                new_grid[guard_loc[0]+dh][guard_loc[1]+dw] = '#'
            else:
                guard_loc = [guard_loc[0]+dh, guard_loc[1]+dw]
                if new_grid[guard_loc[0]][guard_loc[1]] != 'X':
                    new_grid[guard_loc[0]][guard_loc[1]] = 'X'
                    dist_locs += 1
        steps += 1
        if verbose:
            print_grid(new_grid)
            print()
    if verbose:
        print("Steps:", steps)
    return dist_locs, new_grid

def guard_obs(text, max_steps=100, verbose=False) -> int:
    grid: list = [[c for c in line] for line in text]
    _, path = guard_path(text)
    new_grid: list = deepcopy(path)
    n_obstacles: int = 0
    for i, line in enumerate(path):
        for j, c in enumerate(line):
            if c == 'X' and not grid[i][j] in '^>v<':
                tmp_grid: list = deepcopy(grid)
                tmp_grid[i][j] = '#'
                n, _ = guard_path(grid_to_text(tmp_grid).split(), max_steps=max_steps, verbose=False)
                if n:
                    pass
                else:
                    new_grid[i][j] = 'O'
                    n_obstacles += 1
            else:
                pass
    if verbose:
        print_grid(new_grid)
    return n_obstacles, new_grid


if guard_path(input_test1, verbose=True)[0] == 41:
    print("Part I:", guard_path(input_6, verbose=False)[0], '\n\n')

if guard_obs(input_test1, verbose=True)[0] == 6:
    print("Part II:", guard_obs(input_6, max_steps=10000)[0])
