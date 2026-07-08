from colorama import init, Fore, Style
# import re
# from pprint import pprint

init(autoreset=True)

"""
Use the pattern `_5` to process with the desired date.
"""

input_test: str = \
"""3-5
   10-14
   16-20
   12-18
   
   1
   5
   8
   11
   17
   32
   """.replace('   ', '')

input_5: str = open("input_5").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    day = "Day 5"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 0
    # complete this function
    ranges, ids = [n.split() for n in text.split("\n\n")]
    fresh = []#set()
    for id in ids:
        for r in ranges:
            ends = [int(_) for _ in r.split("-")]
            if part == 2:
                total += ends[1] - ends[0] + 1
                for f in fresh:
                    if ends[0] < f[0] and ends[1] > f[1]:
                        total -= f[1] - f[0] + 1
                        fresh[fresh.index(f)] = [0, 0]
                    elif ends[0] > f[0] and ends[1] < f[1]:
                        total -= ends[1] - ends[0] + 1
                        ends = [0, 0]
                        break
                    elif f[0] <= ends[0] <= f[1] <= ends[1]:
                        total -= f[1] - ends[0] + 1
                        ends = [f[1]+1, ends[1]]
                    elif ends[0] <= f[0] <= ends[1] <= f[1]:
                        total -= ends[1] - f[0] + 1
                        ends = [ends[0], f[0]-1]
                #for _ in range(ends[0], ends[1]+1):
                #    #fresh.add(_)
                #    total += 1
                #    for f in fresh:
                #        if _ >= f[0] and _ <= f[1]:
                #            total -= 1
                #            break
                    #if not _ in fresh:
                    #    fresh.append(_)
                    #total += ends[1] - ends[0] + 1
                fresh.append(ends)
                continue
            if int(id) >= ends[0] and int(id) <= ends[1]:
                total += 1
                break
        if part == 2:
            # total += len(fresh)
            break
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
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_5, (input_test, 3), part=1)
    run_test(input_5, (input_test, 14), part=2)
    
