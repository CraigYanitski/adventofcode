from colorama import init, Fore, Style
import re
from pprint import pprint
from copy import deepcopy
from functools import lru_cache

init(autoreset=True)

input_test: str = \
"""r, wr, b, g, bwu, rb, gb, br

   brwrr
   bggr
   gbbr
   rrbgbr
   ubwu
   bwurrg
   brgr
   bbrgwb
""".replace('   ', '')

input_19: str = open("input_19").read()


def solve(text, test=False, part=1, verbose=False) -> int:
    total: int = 0
    global towels
    towels, patterns = text.split('\n\n')
    towels = towels.strip().split(', ')
    patterns: list = patterns.strip('\n').splitlines()
    #print(towels)
    print(','.join(towels))
    print()
    print('\n'.join(patterns))
    print()
    for pattern in patterns:
        if verbose:
            print(pattern)
        res: int = match_pattern(pattern, part=part)
        if verbose:
            print(res)
        total += res
    return total

@lru_cache(maxsize=None)
def match_pattern(pattern, part=1) -> int:
    global towels
    if pattern == '':
        return 1
    total: int = 0
    for towel in towels:
        if towel == pattern:
            total += 1
            if part == 1:
                return 1
        elif pattern.startswith(towel):
            total += match_pattern(pattern[len(towel):], part=part)
            if part == 1 and total:
                return 1
    return total


def run_test(text, test_inputs=('', 0), part=1) -> None:
    res: int = solve(test_inputs[0], test=True, part=part, verbose=True)
    print()
    if res == test_inputs[1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        match_pattern.cache_clear()
        res: int = solve(text, part=part, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
    print()
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_19, (input_test, 6), part=1)
    print('\n' + '='*10 + '\n')
    run_test(input_19, (input_test, 16), part=2)
    
