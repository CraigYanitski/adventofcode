from colorama import init, Fore, Style
import re
#from pprint import pprint

import heapq
from z3 import IntVector, Int, Optimize

init(autoreset=True)

"""
Use the pattern `_10` to process with the desired date.
"""

input_test: str = \
"""[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
   [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
   [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
   """.replace('   ', '')

input_error = "[.#...#..] (1,3,5,6,7) (1,3,4,5,6) (1,5) (1,7) (0,1,2,5,6,7) (0,5) (0,1,2,3,4,7) (1,3,4,5,6,7) {13,38,11,7,7,20,18,31}"

input_10: str = open("input_10").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    day = "Day 10"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 0
    # complete this function
    lines = text.strip().split("\n")

    for i, machine in enumerate(lines):
        if verbose:
            print(f"\r{i+1:>3}/{len(lines)}")
        if verbose:
            print("machine:", machine)
        indicators = re.search(r"\[(.*?)\]", machine).group(1)
        buttons = [m.split(",") for m in re.findall(r"\((.*?)\)", machine)]
        joltage = [int(j) for j in (re.search(r"\{(.*?)\}", machine).group(1)).split(",")]
        if verbose:
            print("indicators:", indicators)
            print("buttons:", buttons)
            print("joltage:", joltage)
        ind_flags = get_bits(indicators)
        button_flags = get_button_bits(buttons, len(indicators))
        max_flags = get_bits("#" * len(indicators))
        if verbose:
            print("indicator flags:", ind_flags)
            print("button flags:", button_flags)
            print("max flags:", max_flags)
        if part == 1:
            test = []
            #min_p = len(indicators)
            for b in button_flags:
                heapq.heappush(test, [1, b])
            total += test_sol(ind_flags, button_flags, len(indicators))
        else:
            cs = [[] for _ in range(len(joltage))]
            for b, button in enumerate(buttons):
                for c in button:
                    cs[int(c)].append(b)
            btn = IntVector("btn", len(buttons))
            presses = Int("presses")
            s = Optimize()
            for c in range(len(cs)):
                s.add(sum(btn[b] for b in cs[c]) == joltage[c])
            for b in range(len(buttons)):
                s.add(btn[b] >= 0)
            s.add(sum(btn) == presses)
            s.minimize(presses)
            s.check()
            m = s.model()
            presses = m.eval(presses).as_long()
            total += presses
        # while len(test) > 0:
        #     n, ind_test = heapq.heappop(test)
        #     #print("n:", n, "ind test:", ind_test)
        #     if ind_test == ind_flags:
        #         min_p = min(min_p, n)
        #         continue
        #     if n > len(button_flags):
        #         print(f"failed to solve {machine}")
        #         break
        #     elif min_p <= n:#and n > min_p:
        #         print("Found solution:", min_p)
        #         total += min_p#test_sol(ind_flags, button_flags, len(indicators))
        #         print("Total:", total, "\n")
        #         break
        #     if ind_test != ind_flags:
        #         for b in button_flags:
        #             bn = n + 1
        #             if bn > min_p:
        #                 continue
        #             bind = (max_flags & ind_test) ^ (max_flags & b)
        #             #print(bn, bind)
        #             if bind == ind_flags:
        #                 if verbose:
        #                     print("solution:", bn, bind)
        #                 ind_test = bind
        #                 #print(min_p, bn)
        #                 min_p = min(min_p, bn)
        #                 heapq.heappush(test, [bn, bind])
        #                 break
        #             #print("pushing:", [bn, bind])
        #             heapq.heappush(test, [bn, bind])
        #print("total:", total)
        if verbose:
            print()
        #del test
        #input()
    return total

def test_sol(res, buttons, length):
    sols = [-1]*(1<<length); sols[0] = 0
    test = [0]
    for t in test:
        for op in buttons:
            #print(t^op)
            if ~sols[t^op]: continue
            sols[t^op] = sols[t]+1; test.append(t^op)
    return sols[res]

def get_button_bits(buttons, length=1):
    ind_flags_list = []
    for button in buttons:
        ind_flags = ["."] * length
        for i in button:
            ind_flags[int(i)] = "#"
        ind_flags_list.append(get_bits("".join(ind_flags)))
    return ind_flags_list

def get_bits(string):
    return int("0b" + "".join("1" if c == "#" else "0" for c in list(string)), 2)


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
    run_test(input_10, (input_test, 7), part=1)
    run_test(input_10, (input_test, 33), part=2)
    
