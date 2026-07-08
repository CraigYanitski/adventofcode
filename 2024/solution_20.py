from colorama import init, Fore, Style
import re
from pprint import pprint
import heapq
import sys

init(autoreset=True)

input_test: str = \
"""###############
   #...#...#.....#
   #.#.#.#.#.###.#
   #S#...#.#.#...#
   #######.#.#.###
   #######.#.#...#
   #######.#.###.#
   ###..E#...#...#
   ###.#######.###
   #...###...#...#
   #.#####.#.###.#
   #.#...#.#.#...#
   #.#.#.#.#.#.###
   #...#...#...###
   ###############
""".replace('   ', '')

input_20: str = open("input_20").read()


class Dijkstra:
    def __init__(self, map_):
        self.map: list = map_
        self.width: int = len(map_[0])
        self.height: int = len(map_)
        self.distances: dict = {(x, y): float('inf') for y in range(self.height) for x in range(self.width)}
        self.cheat: dict = dict()
        for y, line in enumerate(self.map):
            if 'S' in line:
                self.start: tuple = (line.index('S'), y)
                self.distances[self.start] = 0
            if 'E' in line:
                self.end: tuple = (line.index('E'), y)
        return
    
    def find_shortest_path(self, cheat=False, dist=2, verbose=False):
        #print(self.distances)
        priority_queue: list = [(0, self.start)]
        cheat_section: None|tuple = None
        while priority_queue:
            cur_distance, cur_pos = heapq.heappop(priority_queue)
            x, y = cur_pos
            if not self.is_valid(cur_pos):
                continue
            if cur_distance < self.distances[(x, y)]:
                self.distances[(x, y)] = cur_distance
            for pos in ((x+1, y), (x, y-1), (x-1, y), (x, y+1)):
                x_next, y_next = pos
                dx, dy = x_next-x, y_next-y
                distance: int = cur_distance + 1
                if not self.is_valid(pos):
                    continue
                if distance <= self.distances[pos]:
                    # if cheat:
                    #     print(pos)
                    if (self.map[y_next][x_next] == '#') \
                            and (not (cur_pos, pos) in self.cheat.keys()) \
                            and self.is_valid_track((pos[0]+dx, pos[1]+dy), distance=distance+1) \
                            and cheat:
                        cheat_section: None|tuple = (cur_pos, pos)
                        self.cheat[cheat_section] = self.distances[(pos[0]+dx, pos[1]+dy)] - (distance+1)
                        continue
                    elif self.map[y_next][x_next] == '#':
                        continue
                    heapq.heappush(priority_queue, (distance, pos))
        if verbose:
            for y in range(self.height):
                for x in range(self.width):
                    if self.distances[x, y] == float("inf"):
                        prefix = Style.DIM + Fore.RED
                    else:
                        prefix = Style.BRIGHT
                    print(prefix + f'{self.distances[x, y]}'.center(5), end='')
                print()
        return

    def find_cheats(self, lim=100, dist=2, verbose=False):
        self.find_shortest_path()
        base: int = self.distances[self.end]
        print(f"base distance: {base}")
        total: int = 0
        self.find_shortest_path(cheat=True, dist=dist, verbose=verbose)
        cheats = []
        cheat_dict = {}
        for c in self.cheat.items():
            #if c[1] != float("inf"):
            cheats.append(c)
            if c[1] in cheat_dict.keys():
                cheat_dict[c[1]] += 1
            else:
                cheat_dict[c[1]] = 1
            if lim <= c[1] < float("inf"):
                total += 1
        #pprint(sorted(cheats, key=lambda x: x[1]))
        if verbose:
            pprint(sorted(cheat_dict.items(), key=lambda x: x[0]))
        return total

    def is_valid(self, pos):
        return 0<=pos[0]<self.width and 0<=pos[1]<self.height

    def is_valid_wall(self, pos):
        if self.is_valid(pos):
            return self.map[pos[0]][pos[1]] == '#'
        return False

    def is_valid_track(self, pos, distance=None):
        if self.is_valid(pos):
            if not distance is None:
                short: bool = distance <= self.distances[pos]
            else:
                short: bool = True
            return (self.map[pos[1]][pos[0]] != '#') and short
        return False

    def reset(self):
        self.distances: dict = {(x, y): float('inf') for y in range(self.height) for x in range(self.width)}
        return


def solve(text, part=1, test=False, verbose=False) -> int:
    total: int = 0
    map_: list = list(map(list, text.splitlines()))
    dijk: Dijkstra = Dijkstra(map_)
    print(f"{dijk.width} X {dijk.height}")
    total: int = dijk.find_cheats(lim=100, verbose=verbose)
    #cheats: dict = {}
    #base: int = dijk.cheat[()]
    #for sec in dijk.cheat.keys():
    #    dist: int = base - dijk.cheat[sec]
    #    if not dist in cheats.keys():
    #        cheats[dist] = 1
    #    else:
    #        cheats[dist] += 1
    #pprint(list(dijk.cheat))
    return total


def run_test(text, test_inputs=('', 0), part=1) -> None:
    res: int = solve(test_inputs[0], test=True, part=part, verbose=True)
    print()
    if res == test_inputs[1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        res: int = solve(text, part=part, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
    print()
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_20, (input_test, 0), part=1)
    #run_test(input_20, (input_test, 12), part=2)
    
