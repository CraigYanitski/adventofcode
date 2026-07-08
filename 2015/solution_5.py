from colorama import init, Fore, Style
import re
#from pprint import pprint

init(autoreset=True)

"""
Use the pattern `_5` to process with the desired date.
"""

day = "day 5"

input_test: str = \
"""ugknbfddgicrmopn
   aaa
   jchzalrnumimnmhp
   haegwjzuvuyypxyu
   dvszwmarrgswjxmb
   """.replace('   ', '')

input_test_2 = \
"""xyxy
   abcdefeghi
   """.replace("   ", "")

input_5: str = open("input_5").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    total: int = 0
    # complete this function
    strings = text.strip().split("\n")
    for s in strings:
        if part == 2:
            t = int(rule4(s) and rule5(s))
        else:
            t = int(rule1(s) and rule2(s) and rule3(s))
        if verbose:
            print(s, total)
        total += t
    return total

def rule1(s):
    return len(re.findall(r"[aeiou]{1}", s)) >= 3
    
def rule2(s):
    return len(re.findall(r"([a-z]{1})\1+", s)) > 0

def rule3(s):
    return len(re.findall(r"(ab|cd|pq|xy)", s)) == 0

def rule4(s):
    return len(re.findall(r"([a-z]{2}).*\1", s)) > 0

def rule5(s):
    return len(re.findall(r"([a-z]{1}).\1", s)) > 0


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
    run_test(input_5, (input_test, 2), part=1)
    run_test(input_5, (input_test_2, 1), part=2)
    
