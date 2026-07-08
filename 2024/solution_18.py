from colorama import init, Fore, Style
import re
from pprint import pprint
from solution_16 import Dijkstra

init(autoreset=True)

input_test: str = \
"""5,4
   4,2
   4,5
   3,0
   2,1
   6,3
   2,4
   1,5
   0,6
   3,3
   2,6
   5,1
   1,2
   5,5
   2,5
   6,5
   1,4
   0,4
   6,4
   1,1
   6,1
   1,0
   0,5
   1,6
   2,0
""".replace('   ', '')

input_18: str = open("input_18").read()

def wrapper(text, part=1, test=False, verbose=False) -> (int|tuple):
    if test:
        n_c: int = 12
    else:
        n_c: int = 1024
    total: int|tuple = navigate_memory(text, n_c, part=part, test=test, verbose=verbose)
    while type(total) == int and part == 2:
        n_c += 1
        total: int|tuple = navigate_memory(text, n_c, part=part, test=test, verbose=verbose)
    return total

def navigate_memory(text, n_corrupt, part=1, test=False, verbose=False) -> int:
    start = (0, 0)
    if test:
        width, height = (7, 7)
        end = (6, 6)
        if part == 1:
            n_corrupt = 12
    else:
        width, height = (71, 71)
        end = (70, 70)
        if part == 1:
            n_corrupt = 1024
    map_: list = []
    for _ in range(height):
        map_.append(list('.' for i in range(width)))
    corrupted: list = list(map(lambda x: tuple(map(int, x.split(','))), text.strip('\n').split('\n')))
    print(f"# of corrupted bytes: {len(corrupted)}")
    for c in corrupted[:n_corrupt]:
        map_[c[1]][c[0]] = '#'
    map_: list = list(map(''.join, map_))
    dijk: Dijkstra = Dijkstra(map_, start, end, move=1, turn=0)
    total: int = dijk.find_shortest_path((1, 0))[0]
    print(n_corrupt, total)
    if total == float('inf'):
        return corrupted[n_corrupt-1]
    if verbose:
        dijk.print_map()
    #total: int = 0
    return total


def run_test(text, test_inputs=('', 0), part=1) -> None:
    res: int|tuple = wrapper(test_inputs[0], test=True, part=part, verbose=True)
    print()
    if res == test_inputs[1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        res: int|tuple = wrapper(text, test=False, part=part, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
    print()
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_18, (input_test, 22), part=1)
    print('\n' + '='*10 + '\n')
    run_test(input_18, (input_test, (6, 1)), part=2)
    
