from colorama import init, Fore, Style
#import re
#from pprint import pprint
import itertools

init(autoreset=True)

"""
Use the pattern `_3` to process with the desired date.
"""

input_test: str = \
"""987654321111111
   811111111111119
   234234234234278
   818181911112111
   """.replace('   ', '')

input_3: str = open("input_3").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if test or verbose or part == 1:
        pass
    day = "Day 3"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 0
    # complete this function
    banks = text.split()
    t = "0"
    for bank in banks:
        if part == 1:
            t = find_max(bank, 2)
        else:
            t = find_max(bank, 12)
        if verbose:
            print(t)
        total += int(t)
    return total

def find_max(digits, length):
    t = list(digits[-length:])
    for d in digits[::-1][length:]:
        idx = 0
        while d >= t[idx]:
            s = t[idx]
            t[idx] = d
            d = s
            idx += 1
            if idx == length:
                break
    m = ''.join(t)
    return m


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
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_3, (input_test, 357), part=1)
    run_test(input_3, (input_test, 3121910778619), part=2)
    
