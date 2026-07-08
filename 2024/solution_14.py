from colorama import init, Fore, Style
import re
from pprint import pprint

init(autoreset=True)

input_test: str = \
"""p=0,4 v=3,-3
   p=6,3 v=-1,-3
   p=10,3 v=-1,2
   p=2,0 v=2,-1
   p=0,0 v=1,3
   p=3,0 v=-2,-2
   p=7,6 v=-1,-3
   p=3,0 v=-1,-2
   p=9,3 v=2,3
   p=7,3 v=-1,2
   p=2,4 v=2,-3
   p=9,5 v=-3,-3
""".replace('   ', '')

input_14: str = open("input_14").read()

def robot_paths(text, time=100, test=False, part=1, verbose=False) -> int:
    robots: list = re.findall("p=(\d+),(\d+) v=(-?\d+),(-?\d+)", text)
    robots = list(map(lambda x: list(map(int, x)), robots))
    if test:
        width, height = (11, 7)
        x_mid, y_mid = (width//2, height//2)
    else:
        width, height = (101, 103)
        x_mid, y_mid = (width//2, height//2)
    if part == 2:
        time = 10000000
    for _ in range(1, time+1):
        tul: int = 0
        tur: int = 0
        tbl: int = 0
        tbr: int = 0
        current_positions = set()
        if part == 2:
            map_: list = list(list('.' for _ in range(101)) for _ in range(103))
        for robot in robots:
            x, y, vx, vy = robot
            if verbose and _ == 100:
                print(f"x={x}, y={y}, vx={vx}, vy={vy}")
            x_end: int = (x + vx*_) % width
            y_end: int = (y + vy*_) % height
            current_positions.add((x_end, y_end))
            if part == 2:
                map_[y_end][x_end] = 'X'
            if x_end < x_mid and y_end < y_mid:
                tul += 1
            if x_end > x_mid and y_end < y_mid:
                tur += 1
            if x_end < x_mid and y_end > y_mid:
                tbl += 1
            if x_end > x_mid and y_end > y_mid:
                tbr += 1
        if part == 2:
            lines: list = list(map(lambda x: ''.join(map(str, x)), map_))
            # Flag on image
            if len(current_positions) == len(robots):#any(('XXXXXXXXXXXXXXX' in line) for line in lines):
                print('\n'.join(''.join(line) for line in map_))
                print(f"time of left/right symmetry: {_}s")
                break
    total: int = tul*tur*tbl*tbr
    if verbose:
        print(total)
    return total

def run_test(text, test_inputs=('', 0), part=1) -> None:
    res: int = robot_paths(test_inputs[0], test=True, part=1, verbose=True)
    print()
    if res == test_inputs[1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        res: int = robot_paths(text, part=part, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
    print()
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_14, (input_test, 12), part=1)
    run_test(input_14, (input_test, 12), part=2)
    
