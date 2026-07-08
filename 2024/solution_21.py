from colorama import init, Fore, Style
import re
from pprint import pprint

init(autoreset=True)

input_test: str = \
"""029A
   980A
   179A
   456A
   379A
""".replace('   ', '')

input_21: str = open("input_21").read()

dir_pad: list = [[' ', '^', 'A'],
                 ['<', 'v', '>']]

num_pad: list = [['7', '8', '9'],
                 ['4', '5', '6'],
                 ['1', '2', '3'],
                 [' ', '0', 'A']]


def solve(text, part=1, test=False, verbose=False) -> int:
    total: int = 0
    codes = text.splitlines()
    px3, px2, px1 = 'A', 'A', 'A'
    for code in codes:
        print(code, ': ', end='')
        dirs1, px1 = control_pad(code, num_pad, pointer=px1)
        dirs2, px2 = control_pad(dirs1, dir_pad, pointer=px2)
        dirs3, px3 = control_pad(dirs2, dir_pad, pointer=px3)
        print(len(dirs3), '*', int(code[:-1]))
        # print(dirs1)
        # print(dirs2)
        # print(dirs3)
        print_dirs(dirs1, dirs2, dirs3)
        complexity: int = int(code[:-1]) * len(dirs3)
        total += complexity
        print()
    return total

def print_dirs(dirs1, dirs2, dirs3):
    d1, d2, d3 = [], [], []
    i1, i2, i3 = 0, 0, 0
    for _ in dirs1:
        m: int = i2 + dirs2[i2:].index('A') + 1
        n: int = i3 + find_substr(dirs3[i3:], 'A', m-i2)
        d1.append(_.rjust(n-i3+2))
        d2.append(dirs2[i2:m].rjust(n-i3+2))
        d3.append(dirs3[i3:n].rjust(n-i3+2))
        i2: int = m
        i3: int = n
    print(''.join(d1))
    print(''.join(d2))
    print(''.join(d3))
    return

def find_substr(string, substr, n) -> int:
    idx: int = 0
    while n:
        idx += string[idx:].index(substr) + 1
        n -= 1
    return idx

def control_pad(output, pad, pointer='A') -> tuple:
    inp: str = ''
    temp = 0
    for n in output:
        x_init, y_init = locate_button(pointer, pad)
        x, y = calculate_manhattan((x_init, y_init),
                                   locate_button(n, pad))
        if pad[y_init][x+x_init] == ' ':
            if y < 0:
                inp += '^'*-y
                y -= y
            else:
                inp += 'v'*y
                y -= y
        elif pad[y+y_init][x_init] == ' ':
            if x < 0:
                inp += '<'*-x
                x -= x
            else:
                inp += '>'*x
                x -= x
        if True:#pad == dir_pad:
            if x < 0:
                inp += '<'*-x
            if x > 0:
                inp += '>'*x
            if y > 0:
                inp += 'v'*y
            if y < 0:
                inp += '^'*-y
        else:
            if y > 0:
                inp += 'v'*y
            if y < 0:
                inp += '^'*-y
            if x < 0:
                inp += '<'*-x
            if x > 0:
                inp += '>'*x
        #if temp < 0:
        #    inp += '<'
        #elif temp > 0:
        #    inp += '>'
        inp += 'A'
        pointer = n
    return inp, pointer

def locate_button(i: str, pad: list) -> tuple:
    for y, line in enumerate(pad):
        if i in line:
            x: int = line.index(i)
            break
    return x, y

def calculate_manhattan(pos1, pos2) -> tuple:
    return pos2[0]-pos1[0], pos2[1]-pos1[1]


def run_test(text, test_inputs=('', 0), part=1) -> None:
    res: int = solve(test_inputs[0], test=True, part=1, verbose=True)
    print()
    if res == test_inputs[1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        res: int = solve(text, part=part, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
    print()
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_21, (input_test, 126384), part=1)
    #run_test(input_21, (input_test, 12), part=2)
    
