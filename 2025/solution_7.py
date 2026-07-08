from colorama import init, Fore, Style
import re
#from pprint import pprint
from collections import deque
from functools import lru_cache

init(autoreset=True)

"""
Use the pattern `_7` to process with the desired date.
"""

input_test: str = \
""".......S.......
   ...............
   .......^.......
   ...............
   ......^.^......
   ...............
   .....^.^.^.....
   ...............
   ....^.^...^....
   ...............
   ...^.^...^.^...
   ...............
   ..^...^.....^..
   ...............
   .^.^.^.^.^...^.
   ...............
   """.replace('   ', '')

input_7: str = open("input_7").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    day = "Day 7"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 0
    # complete this function
    if text[-1] != "\n":
        text += "\n"
    # print(text)
    w = text.index("\n")
    levels = text.split()

    @lru_cache
    def tachyon(y, x):
        if levels[y][x] == "S":
            return 1
        parents = [0, 0]
        for _ in range(y-1, -1, -1):
            if levels[_][x] == "S":
                return 1
            elif levels[_][x] == "^":
                break
            if (x > 0) and (levels[_][x-1] == "^"):
                parents[0] += tachyon(_, x-1)
            if (x < (w-1)) and (levels[_][x+1] == "^"):
                parents[1] += tachyon(_, x+1)
        return sum(parents)

    if part == 1:
        starters = [m.start() for m in re.finditer(r"\^", text)]
    else:
        starters = list(range((len(levels)-1) * (w+1), (len(levels)-0)*(w+1) - 1))
    for splitter in starters:
        y = splitter // (w+1)
        x = splitter % (w+1)
        if verbose:
            print(x, y)
            print(tachyon(y, x))
        if part == 1:
            total += int(bool(tachyon(y, x)))
        else:
            total += tachyon(y, x)
    return total


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
    run_test(input_7, (input_test, 21), part=1)
    run_test(input_7, (input_test, 40), part=2)
    
