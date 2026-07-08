from colorama import init, Fore, Style
#import re
#from pprint import pprint

init(autoreset=True)

"""
Use the pattern `_n_` to process with the desired date.
"""

input_test: str = \
"""..@@.@@@@.
   @@@.@.@.@@
   @@@@@.@.@@
   @.@@@@..@.
   @@.@@@@.@@
   .@@@@@@@.@
   .@.@.@.@@@
   @.@@@.@@@@
   .@@@@@@@@.
   @.@.@@@.@.""".replace('   ', '')

input_4: str = open("input_4").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if test or verbose or part:
        pass
    day = "Day 4"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 0
    # complete this function
    rows = text.split()
    if part == 2:
        temp_count = 1
        clearing = False
        while True:
            if verbose and clearing:
                print('\n'.join(rows))
                print()
            rows, temp_count = clear_rolls(rows, clearing)
            if temp_count == 0 and not clearing:
                break
            total += temp_count
            if temp_count > 0:
                clearing = True
            else:
                clearing = False
    else:
        rows, total = clear_rolls(rows, False)
    if verbose:
        print('\n'.join(rows))
    return total

def clear_rolls(rows, remove):
    temp_count = 0
    for i in range(len(rows)):
        for j in range(len(rows[0])):
            c = 0
            if rows[i][j] != "@":
                if remove:
                    rows[i] = rows[i][:j] + "." + rows[i][j+1:]
                continue
            elif remove:
                continue
            if i > 0:
                c += int(rows[i-1][j] != ".")
                if j > 0:
                    c += int(rows[i-1][j-1] != ".")
                if j < (len(rows[0]) - 1):
                    c += int(rows[i-1][j+1] != ".")
            if i < (len(rows) - 1):
                c += int(rows[i+1][j] != ".")
                if j > 0:
                    c += int(rows[i+1][j-1] != ".")
                if j < (len(rows[0]) - 1):
                    c += int(rows[i+1][j+1] != ".")
            if j > 0:
                c += int(rows[i][j-1] != ".")
            if j < (len(rows[0]) - 1):
                c += int(rows[i][j+1] != ".")
            if c < 4:
                temp_count += 1
                #if remove:
                #    rows[i] = rows[i][:j] + "." + rows[i][j+1:]
                #else:
                rows[i] = rows[i][:j] + "x" + rows[i][j+1:]
    return rows, temp_count


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
    run_test(input_4, (input_test, 13), part=1)
    run_test(input_4, (input_test, 43), part=2)
    
