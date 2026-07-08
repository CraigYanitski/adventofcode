from colorama import init, Fore, Style
#import re
#from pprint import pprint

from collections import defaultdict, deque

init(autoreset=True)

"""
Use the pattern `_11` to process with the desired date.
"""

input_test: str = \
"""aaa: you hhh
   you: bbb ccc
   bbb: ddd eee
   ccc: ddd eee fff
   ddd: ggg
   eee: out
   fff: out
   ggg: out
   hhh: ccc fff iii
   iii: out
   """.replace('   ', '')

input_test_2 = \
"""svr: aaa bbb
   aaa: fft
   fft: ccc
   bbb: tty
   tty: ccc
   ccc: ddd eee
   ddd: hub
   hub: fff
   eee: dac
   dac: fff
   fff: ggg hhh
   ggg: out
   hhh: out
   """.replace("   ", "")

input_11: str = open("input_11").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    day = "Day 11"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 0
    # complete this function
    lines = text.strip().split("\n")
    connections = defaultdict(list)
    for line in lines:
        m, cs = line.split(": ")
        for c in cs.split():
            connections[m].append(c)
    if part == 2:
        t = 1
        for start, end, avoid in (("svr", "dac", "fft out"), ("dac", "fft", "svr out"), ("fft", "out", "svr dac")):
            t *= count_paths(connections, start, end, avoid)
        total += t
        t = 1
        for start, end, avoid in (("svr", "fft", "dac out"), ("fft", "dac", "svr out"), ("dac", "out", "svr fft")):
            t *= count_paths(connections, start, end)
        total += t
    else:
        total = count_paths(connections, "you", "out")
    return total

def list_nodes(connections):
    senders = defaultdict(int)
    queue = deque()
    nodes = []

    for cs in connections.values():
        for c in cs:
            senders[c] += 1
    for m in connections.keys():
        if not m in senders:
            senders[m] = 0
    for m, cs in senders.items():
        if not cs:
            queue.append(m)
    while queue:
        m = queue.popleft()
        nodes.append(m)
        if m in connections:
            for c in connections[m]:
                senders[c] -= 1
                if not senders[c]:
                    queue.append(c)
    return nodes

def count_paths(connections, start, end, avoid=""):
    nodes = list_nodes(connections)
    paths = {m: 0 for m in nodes}
    paths[start] = 1
    for m in nodes:
        if m in connections:
            for c in connections[m]:
                paths[c] += paths[m]
    return paths[end]

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
    run_test(input_11, (input_test, 5), part=1)
    run_test(input_11, (input_test_2, 2), part=2)
    
