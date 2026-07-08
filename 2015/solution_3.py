from colorama import init, Fore, Style
#import re
#from pprint import pprint

init(autoreset=True)

"""
Use the pattern `_3` to process with the desired date.
"""

day = "day 3"

input_test: str = \
"""^v
   ^>v<
   ^v^v^v^v^v""".replace('   ', '')

input_3: str = open("input_3").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    total: int = 0
    # complete this function
    lines = text.strip().split("\n")
    robo = False
    for direction in lines:
        pos = [0, 0]
        pos_santa = [0, 0]
        pos_robot = [0, 0]
        positions = set()
        positions.add(tuple(pos))
        for d in direction:
            match d:
                case "^":
                    pos[1] += 1
                case ">":
                    pos[0] += 1
                case "v":
                    pos[1] -= 1
                case "<":
                    pos[0] -= 1
                case _:
                    print(f"Unexpected direction '{d}' encountered!")
            positions.add(tuple(pos))
            if part == 2:
                if robo:
                    pos_robot = pos
                    pos = pos_santa
                    robo = False
                else:
                    pos_santa = pos
                    pos = pos_robot
                    robo = True
        total += len(positions)
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
    run_test(input_3, (input_test, 8), part=1)
    run_test(input_3, (input_test, 17), part=2)
    
