from colorama import init, Fore, Style
#import re
#from pprint import pprint

init(autoreset=True)

"""
Use the pattern `_1` to process with the desired date.
"""

day = "day 1"

input_test: str = \
"""))(((((""".replace('   ', '')

input_test_2 = "()())"

input_1: str = open("input_1").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    total: int = 0
    # complete this function
    directions = text.replace("\n", "")
    for i, d in enumerate(directions, 1):
        if d == "(":
            total += 1
        elif d == ")":
            total -= 1
        else: pass
        if total < 0 and part == 2:
            return i
    return total


def run_test(text, test_inputs=('', 0), part=1) -> None:
    print(f"{day}\n{'-'*len(day)}")
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
    run_test(input_1, (input_test, 3), part=1)
    run_test(input_1, (input_test_2, 5), part=2)
    
