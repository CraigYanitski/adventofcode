from colorama import init, Fore, Style
import re
from pprint import pprint
import numpy as np

init(autoreset=True)

input_test: str = \
"""1
   10
   100
   2024
""".replace('   ', '')

input_test_2: str = \
"""1
   2
   3
   2024
""".replace('   ', '')

input_22: str = open("input_22").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    total: int = 0
    nums_init: list = text.splitlines()
    print(len(nums_init))
    if part == 1:
        for num in nums_init:
            total += compute_secret_number(int(num), 2000)
    else:
        tot = np.zeros(2000, dtype=int)
        dat: list = []
        for num in nums_init:
            l: list =  list(map(lambda x: int(str(compute_secret_number(int(num), x))[-1]), range(1, 2001)))
            dat.append(l)
            print(tot.max())
        total: int = tot.max()
    return total

def compute_secret_number(num, n) -> int:
    i = 0
    while i < n:
        num = num ^ (num << 6) % 16777216
        num = num ^ (num >> 5) % 16777216
        num = num ^ (num << 11) % 16777216
        i += 1
    return num

def find_pattern(arr, pattern):
    i_pat = []
    for line in arr:
        idx = ''.join(map(str, line)).find(pattern)
        if idx > -1:
            i_pat.append(idx+len(pattern))
        else:
            i_pat.append(None)
    return i_pat


def run_test(text, test_inputs=('', 0), part=1) -> None:
    res: int = solve(test_inputs[0], test=True, part=part, verbose=True)
    print()
    if res == test_inputs[1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        res: int = solve(text, part=part, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
    print()
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_22, (input_test, 37327623), part=1)
    print('='*10)
    run_test(input_22, (input_test, 23), part=2)
    
