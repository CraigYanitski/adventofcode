from colorama import init, Fore, Style
#import re
#from pprint import pprint

#import numpy as np

init(autoreset=True)

"""
Use the pattern `_n_` to process with the desired date.
"""

input_test: str = \
"""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
   1698522-1698528,446443-446449,38593856-38593862,565653-565659,
   824824821-824824827,2121212118-2121212124""".replace('   ', '')

input_2: str = open("input_2").read()


def solve(text, part=1, verbose=False) -> int:
    day = "Day 2"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 0
    # complete this function
    ranges = text.replace("\n", "").split(",")
    invalid = []
    for r in ranges:
        if verbose:
            print(f"{r}:")
        start, end = r.split("-")
        if check_invalid(start) and not start in invalid:
            if verbose:
                print(f"    {start}")
            invalid.append(start)
            total += int(start)
        if check_invalid(end) and not end in invalid:
            if verbose:
                print(f"    {end}")
            invalid.append(end)
            total += int(end)
        idx = (len(start)//2)
        if part == 2:
            s = 1
        else:
            s = idx
        for p in range(s, idx+1):
            if len(start) == 1:
                pattern = "1"
            elif bool(len(start)%2) and part == 1:
                pattern = "1" + "0"*p
            else:
                pattern = start[:p]
            if part == 2:
                m = round(len(start)/len(pattern))
            else:
                m = 2
            id = pattern * m
            while int(id) < int(end):
                if int(id) > int(start) and not id in invalid:
                    if verbose:
                        print(f"    {id}")
                    invalid.append(id)
                    total += int(id)
                pattern = str(int(pattern) + 1)
                id = pattern * m
        idx = (len(end)//2)
        if part == 2:
            s = 1
        else:
            s = idx
        for p in range(s, idx+1):
            if len(end) == 1:
                pattern = "1"
            elif bool(len(end)%2) and part == 1:
                pattern = "1" + "0"*p
            else:
                pattern = end[:p]
            if part == 2:
                m = round(len(end)/len(pattern))
            else:
                m = 2
            id = pattern * m
            while int(id) > int(start):
                if int(id) < int(end) and not id in invalid:
                    if verbose:
                        print(f"    {id}")
                    invalid.append(id)
                    total += int(id)
                pattern = str(int(pattern) - 1)
                id = pattern * m
    # for i in invalid:
    #     total += int(i)
    return total

def check_invalid(num):
    digits = str(num)
    if bool(len(digits) % 2) or (len(digits) < 2):
        return False
    if digits[0] == "0":
        return False
    return digits[:len(digits)//2] == digits[len(digits)//2:]


def run_test(text, test_inputs=('', 0), part=1) -> None:
    print()
    res: int = solve(test_inputs[0], part=part, verbose=True)
    if res == test_inputs[1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        print()
        res: int = solve(text, part=part, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
        print()
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_2, (input_test, 1227775554), part=1)
    run_test(input_2, (input_test, 4174379265), part=2)
    
