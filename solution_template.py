from colorama import init, Fore, Style
#import re
#from pprint import pprint

init(autoreset=True)

"""
Use the pattern `_n_` to process with the desired date.
"""

day = "day N_"

input_test: str = \
"""""".replace('   ', '')

input_n_: str = open("input_n_").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    total: int = 0
    # complete this function
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
    run_test(input_n_, (input_test, 0), part=1)
    #run_test(input_n_, (input_test, 0), part=2)
    
