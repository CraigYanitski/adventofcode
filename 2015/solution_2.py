from colorama import init, Fore, Style
#import re
#from pprint import pprint
from itertools import combinations

init(autoreset=True)

"""
Use the pattern `_2` to process with the desired date.
"""

day = "day 2"

input_test: str = \
"""2x3x4
   1x1x10
   """.replace('   ', '')

input_2: str = open("input_2").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    total: int = 0
    # complete this function
    boxes = text.strip().split("\n")
    for box in boxes:
        dim = [int(d) for d in box.split("x")]
        sides = list(combinations(dim, 2))
        areas = list(u*v for u, v in sides)
        perms = list(2*(u+v) for u, v in sides)
        volume = dim[0] * dim[1] * dim[2]
        if part == 1:
            total += 2 * sum(areas) + min(areas)
        else:
            total += min(perms) + volume
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
    print(f"{day}\n{'-'*len(day)}")
    run_test(input_2, (input_test, 101), part=1)
    run_test(input_2, (input_test, 48), part=2)
    
