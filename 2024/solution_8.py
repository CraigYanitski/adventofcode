from copy import deepcopy
from colorama import init, Fore, Style

init(autoreset=True)

input_test1 = \
"""............
   ........0...
   .....0......
   .......0....
   ....0.......
   ......A.....
   ............
   ............
   ........A...
   .........A..
   ............
   ............""".replace('   ', '')

input_test2 = \
"""T.........
   ...T......
   .T........
   ..........
   ..........
   ..........
   ..........
   ..........
   ..........
   ..........""".replace('   ', '')

input_8 = open("input_8").read()

def field(text, resonant=False, verbose=False) -> int:
    lines: list = text.split('\n')
    while '' in lines:
        lines.remove('')
    height: int = len(lines)
    width: int = len(lines[0])
    antennae_num: dict = {}
    antennae_pos: dict = {}
    nodes: dict = {}
    node_field: list = list(list(line) for line in lines)
    new_field: list = list(list(line) for line in lines)
    if verbose:
        print(list(l for l in list(set(text)) if l.isalnum()))
        print(height, width)
    for _ in list(set(text)):
        if not _.isalnum():
            continue
        antennae_num[_] = text.count(_)
        antennae_pos[_] = []
        for i, line in enumerate(lines):
            x: int = 0
            for j in range(line.count(_)):
                x = line.index(_)
                antennae_pos[_].append((i, deepcopy(x)))
        if antennae_num[_] > 1:
            nodes[_] = find_nodes(antennae_pos[_], width, height, resonant=resonant)
        else:
            nodes[_] = []
        for node in nodes[_]:
            node_field[node[0]][node[1]] = '#'
            if new_field[node[0]][node[1]] == '.':
                new_field[node[0]][node[1]] = '#'
    if verbose:
        print_field(new_field)
    return (''.join(list(''.join(line) for line in node_field))).count('#')
        
def find_nodes(antennae, width, height, resonant=False) -> list:
    nodes = []
    for i in range(len(antennae)):
        if resonant:
            nodes.append(antennae[i])
        for j in range(i+1, len(antennae)):
            dx: int = antennae[i][0] - antennae[j][0]
            dy: int = antennae[i][1] - antennae[j][1]
            x1: int = antennae[j][0]-dx
            y1: int = antennae[j][1]-dy
            x2: int = antennae[i][0]+dx
            y2: int = antennae[i][1]+dy
            while 0 <= x1 < height and 0 <= y1 < width:
                nodes.append((x1, y1))
                if not resonant:
                    break
                x1 -= dx
                y1 -= dy
            while 0 <= x2 < height and 0 <= y2 < width:
                nodes.append((x2, y2))
                if not resonant:
                    break
                x2 += dx
                y2 += dy
    return nodes

def print_field(field):
    for line in field:
        for _ in line:
            prefix: str = ''
            if _ == '.':
                prefix = Fore.WHITE + Style.DIM
            elif _ == '#':
                prefix = Fore.RED + Style.DIM
            elif _.isnumeric():
                prefix = Fore.MAGENTA + Style.BRIGHT
            elif _.isalpha():
                prefix = Fore.GREEN + Style.BRIGHT
            print(prefix + _, end='')
        print()
    return


if __name__ == "__main__":
    res: int = field(input_test1, verbose=True)
    if res == 14:
        print(f"Part I passed!! -> test = {res}")
        ans: int = field(input_8, verbose=True)
        print()
        print(f"Part I: {ans}")
        print('='*15)
    res1: int = field(input_test1, resonant=True, verbose=True)
    res2: int = field(input_test2, resonant=True, verbose=True)
    if res1 == 34 and res2 == 9:
        print(f"Part II passed!! -> test = {res1}")
        ans: int = field(input_8, resonant=True, verbose=False)
        print()
        print(f"Part I: {ans}")
        print('='*15)

