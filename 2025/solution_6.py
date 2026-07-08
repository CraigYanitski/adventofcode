from colorama import init, Fore, Style
import re
#from pprint import pprint

init(autoreset=True)

"""
Use the pattern `_6` to process with the desired date.
"""

input_test: str = \
"""123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""#.replace('   ', '')

input_6: str = open("input_6").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if test or part or verbose:
        pass
    day = "Day 6"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 0
    # complete this function
    lines = text.strip().split("\n")
    n_num = len(lines)-1
    idx = []
    for match in re.finditer(r"[\+\*]", lines[-1]):
        if match.start() == 0:
            continue
        idx.append(match.start())
    numerals = []
    for _ in range(n_num):
        numerals.append([])
        e = 0
        for i in idx[::-1]:
            if i == idx[-1]:
                numerals[-1].append(lines[_][i:])
            else:
                numerals[-1].append(lines[_][i:e-1])
            e = i
        numerals[-1].append(lines[_][:e-1])
    operands = lines[-1].split()[::-1]
    for i, op in enumerate(operands):
        if part == 2:
            n_num = len(numerals[-1][i])
            numbers = []
            for _ in range(n_num):
                num = ""
                for n in range(len(numerals)):
                    # if len(numerals[n][i]) < _+1:
                    #     continue
                    num += numerals[n][i][_]
                if num == "":
                    n_num = _
                    break
                numbers.append(num)
        else:
            numbers = []
            for _ in range(n_num):
                numbers.append(numerals[_][i])
        if op == "+":
            t = 0
            for _ in range(n_num):
                if verbose:
                    print(numbers[_])
                t += int(numbers[_])
            if verbose:
                print("+")
        elif op == "*":
            t = 1
            for _ in range(n_num):
                if verbose:
                    print(numbers[_])
                t *= int(numbers[_])
            if verbose:
                print("*")
        else:
            t = 0
        if verbose:
            print(t)
            print()
        total += t
    return total


def run_test(text, test_inputs=('', 0), part=1) -> None:
    print()
    res: int = solve(test_inputs[0], test=True, part=part, verbose=True)
    if res == test_inputs[1]:
        print(Style.BRIGHT + Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        print()
        res: int = solve(text, part=part, verbose=False)
    else:
        print(Style.BRIGHT + Fore.RED + "Part " + 'I'*part + " test failed...")
        print()
    print("Part " + 'I'*part + Style.BRIGHT + f": {res}")


if __name__ == "__main__":
    run_test(input_6, (input_test, 4277556), part=1)
    run_test(input_6, (input_test, 3263827), part=2)
    
