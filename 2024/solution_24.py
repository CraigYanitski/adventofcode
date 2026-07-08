from colorama import init, Fore, Style
import re
from pprint import pprint

init(autoreset=True)

input_test: str = \
"""""".replace('   ', '')

input_24: str = open("input_24").read()


def solve(text, part=1, verbose=False) -> int:
    total: int = 0
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
    run_test(input_24, (input_test, 12), part=1)
    #run_test(input_24, (input_test, 12), part=2)
    
