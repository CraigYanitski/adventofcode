from colorama import init, Fore, Style
#import re
#from pprint import pprint

init(autoreset=True)

"""
Use the pattern `_12` to process with the desired date.
"""

input_test: str = \
"""0:
   ###
   ##.
   ##.
   
   1:
   ###
   ##.
   .##
   
   2:
   .##
   ###
   ##.
   
   3:
   ##.
   ###
   ##.
   
   4:
   ###
   #..
   ###
   
   5:
   ###
   .#.
   ###
   
   4x4: 0 0 0 0 2 0
   12x5: 1 0 1 0 2 2
   12x5: 1 0 1 0 3 2
   """.replace('   ', '')

input_12: str = open("input_12").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    day = "Day 12"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 0
    # complete this function
    groups = text.strip().split("\n\n")
    boxes = []
    for group in groups[:-1]:
        n = group.index("\n")
        boxes.append(group[n+1:].count("#"))
    #for b in boxes:
    #    print(b, "\n")
    for line in groups[-1].split("\n"):
        space, g = line.split(": ")
        gifts = g.split()
        area = eval(space.replace("x", "*"))
        total += area > sum(int(gifts[i])*boxes[i] for i in range(len(boxes)))
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
    run_test(input_12, (input_test, 3), part=1)
    #run_test(input_12, (input_test, 12), part=2)
    
