from colorama import init, Fore, Style
#import re
#from pprint import pprint

import hashlib

init(autoreset=True)

"""
Use the pattern `_4` to process with the desired date.
"""

day = "day 4"

input_test: str = \
"""abcdef
   pqrstuv""".replace('   ', '')

input_4: str = "yzbqklnj"#open("input_4").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    total: int = 0
    # complete this function
    codes = text.strip().split("\n")
    ref = "00000"
    if part == 2 and not test:
        ref += "0"
        print(ref)
    for code in codes:
        i = 0
        while True:
            s = f"{code}{i}"
            h = hashlib.md5(s.encode()).hexdigest()
            if h[:len(ref)] == ref:
                total += i
                break
            i += 1
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
    run_test(input_4, (input_test, 1658013), part=1)
    run_test(input_4, (input_test, 1658013), part=2)
    
