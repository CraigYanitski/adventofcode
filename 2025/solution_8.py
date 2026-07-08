from colorama import init, Fore, Style
#import re
#from pprint import pprint
import heapq
# from functools import lru_cache

import numpy as np

init(autoreset=True)

"""
Use the pattern `_8` to process with the desired date.
"""

input_test: str = \
"""162,817,812
   57,618,57
   906,360,560
   592,479,940
   352,342,300
   466,668,158
   542,29,236
   431,825,988
   739,650,466
   52,470,668
   216,146,977
   819,987,18
   117,168,530
   805,96,715
   346,949,466
   970,615,88
   941,993,340
   862,61,35
   984,92,344
   425,690,689
   """.replace('   ', '')

input_8: str = open("input_8").read()


def solve(text, part=1, test=False, verbose=False) -> int:
    if part or test or verbose:
        pass
    day = "Day 8"
    print(Style.BRIGHT + f"{day}\n{len(day)*'-'}")
    total: int = 1
    # complete this function
    jboxes = text.split()
    positions = []
    connections = []
    circuits = [[_] for _ in range(len(jboxes))]
    for box in jboxes:
        positions.append([int(p) for p in box.split(',')])
    positions = np.array(positions)
    
    if test:
        n_c = 10
    else:
        n_c = 1000
    #while len(connections) < n_c:
    #    d = i = j = 0
    for d, i, j in get_shortest(positions):
        if len(connections) == n_c and part == 1:
            break
        if len(circuits) == 1 and part == 2:
            break
        if len(connections) > 1000 and part == 2:
            dropped = connections.pop()
        # print(d, i, j)
        if (([d, i, j] in connections) or ([d, j, i] in connections)):
            continue
        if not (d + i + j):
            break
        i_c = -1
        j_c = -1
        for _, c in enumerate(circuits):
            if i in c:
                i_c = _
            if j in c:
                j_c = _
            if i_c >= 0 and j_c >= 0:
                break
        # print(d, i, j, i_c, j_c)
        if i_c > -1 and i_c == j_c:
            connections.append([d, i, j])
        elif i_c > -1 and j_c > -1:
            c1 = circuits[i_c]
            c2 = circuits[j_c]
            circuits.remove(c1)
            circuits.remove(c2)
            circuits.append(c1 + c2)
            connections.append([d, i, j])
        elif i_c > -1:
            c = circuits[i_c]
            circuits.remove(c)
            circuits.append(c+[j])
            connections.append([d, i, j])
        elif j_c > -1:
            c = circuits[j_c]
            circuits.remove(c)
            circuits.append(c+[i])
            connections.append([d, i, j])
        else:
            circuits.append([i, j])
            connections.append([d, i, j])
        if verbose:
            print("circuits:", circuits[::-1])
    if verbose:
        print("connections:")
        for c in connections:
            print(f" - {positions[c[1]]} and {positions[c[2]]}  ({c[0]})")
    c_size = []
    for c in circuits:
        c_size.append(len(c))
    if verbose:
        print("circuits:")
        for i, c in enumerate(c_size):
            print(f" - {c}: {circuits[i]}")
    if part == 1:
        for _ in range(3):
            c = max(c_size)
            c_size.remove(c)
            total *= c
    else:
        d, i, j = connections[-1]
        total = positions[i, 0] * positions[j, 0]
    return total

def get_shortest(positions):
    shortest = []
    for i in range(positions.shape[0]):
        # c = []
        # for _ in existing:
        #     if i in _:
        #         c = _
        for j, d in enumerate(find_neighbours(positions, i)):
            if d == 0:
                continue
            heapq.heappush(shortest, [d, i, j])
    while len(shortest):
        yield heapq.heappop(shortest)

# @lru_cache
def find_neighbours(positions, i):
    # idx = np.array([True]*positions.shape[0])
    # idx[i] = False
    distances = np.abs(np.linalg.norm(positions - positions[i], axis=1))
    return distances


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
    run_test(input_8, (input_test, 40), part=1)
    run_test(input_8, (input_test, 25272), part=2)
    
