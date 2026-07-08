from colorama import init, Fore, Style
import re
from pprint import pprint

init(autoreset=True)

"""
Use the pattern `_n_` to process with the desired date.
"""

input_test: str = \
"""L68
   L30
   R48
   L5
   R60
   L55
   L1
   L99
   R14
   L82""".replace('   ', '')

input_1: str = open("input_1").read()


class Dial:
    def __init__(self, num=0, total=100, click=False):
        self.total = total
        self.num = num
        self.count = 0
        self.click = click
        return
    def turn(self, op):
        if not len(op):
            return self.count
        dist = int(op[1:])
        num = 0
        count = 0
        if op[0] == "L":
            num = (self.num - dist) % self.total
            count = int((num > self.num and self.num > 0) or num == 0) + dist//self.total
        elif op[0] == "R":
            num = (self.num + dist) % self.total
            count = int(num < self.num) + dist//self.total
        self.num = num
        if self.click:
            self.count += count
        else:
            self.count += int(num == 0)
        return self.count
    def __str__(self):
        return f"dial: {self.num}, count: {self.count}"


def solve(text, part=1, test=False, verbose=False) -> int:
    total: int = 0
    day = "Day 1"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    ops = text.split("\n")
    if test:
        dial = Dial(50, 100, part==2)
    else:
        dial = 50
    for op in ops:
        if test:
            total = dial.turn(op)
        else:
            dial, t = turn_dial(dial, op, new=part==2)
            total += t
    # print(dial, total)
    print(dial)
    return total


def turn_dial(dial, op, new=False):
    if not len(op):
        return dial, 0
    dist = int(op[1:])
    if op[0] == "L":
        num = (dial - dist) % 100
        if new:
            count = int((num > dial and dial > 0) or (num == 0)) + (dist//100)
        else:
            count = int(num == 0)
    else:
        num = (dial + dist) % 100
        if new:
            count = int(num < dial) + (dist//100)
        else:
            count = int(num == 0)
    return num, count


def run_test(text, test_inputs=('', 0), part=1) -> None:
    print()
    res: int = solve(test_inputs[0], test=False, part=part, verbose=True)
    if res == test_inputs[1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        print()
        res: int = solve(text, part=part, test=False, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
        print()
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_1, (input_test, 3), part=1)
    run_test(input_1, (input_test, 6), part=2)
    
