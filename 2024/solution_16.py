from colorama import init, Fore, Style
import sys
import heapq

sys.setrecursionlimit(5000)

init(autoreset=True)

input_test: str = \
"""###############
   #.......#....E#
   #.#.###.#.###.#
   #.....#.#...#.#
   #.###.#####.#.#
   #.#.#.......#.#
   #.#.#####.###.#
   #...........#.#
   ###.#.#####.#.#
   #...#.....#.#.#
   #.#.#.###.#.#.#
   #.....#...#.#.#
   #.###.#.#.#.#.#
   #S..#.....#...#
   ###############
""".replace('   ', '')

input_test_2 = \
"""#################
   #...#...#...#..E#
   #.#.#.#.#.#.#.#.#
   #.#.#.#...#...#.#
   #.#.#.#.###.#.#.#
   #...#.#.#.....#.#
   #.#.#.#.#.#####.#
   #.#...#.#.#.....#
   #.#.#####.#.###.#
   #.#.#.......#...#
   #.#.###.#####.###
   #.#.#...#.....#.#
   #.#.#.#####.###.#
   #.#.#.........#.#
   #.#.#.#########.#
   #S#.............#
   #################
""".replace('   ', '')

input_test_3: str = \
"""##########
   #.......E#
   #.##.#####
   #..#.....#
   ##.#####.#
   #S.......#
   ##########
""".replace('   ', '')

input_16: str = open("input_16").read()

map_: list = []
paths: list = []
searched: dict = {}
north: tuple = (0, -1)
south: tuple = (0, 1)
east: tuple = (1, 0)
west: tuple = (-1, 0)
directions: tuple = (east, north, west, south)
i_end: tuple = ()


class Dijkstra:
    def __init__(self, map_, start=(0, 0), end=(-1, -1), move=1, turn=0) -> None:
        if len(map_) < 2:
            raise Exception("require a 2D map to initialise.")
        self.map: list = list(map(list, map_))
        self.width: int = len(self.map[0])
        self.height: int = len(self.map)
        self.start: tuple = start
        self.end: tuple = end
        self.move: int = move
        self.turn: int = turn
        self.distances: dict = {((v % self.width, v // self.width), d): float("inf") 
                                for v in range(len(''.join(map_)))
                                for d in directions}
        self.best_route: set = set()
        self.shortest_route: int|float = float('inf')
        # self.print_map()
        return

    def find_shortest_path(self, dir_init, verbose=False) -> tuple:
        self.distances[self.start, dir_init] = 0
        priority_queue: list = [(0, self.start, dir_init, [self.start])]
        while priority_queue:
            current_distance, current_pos, current_dir, current_route = heapq.heappop(priority_queue)
            x, y = current_pos
            if self.map[y][x] == '#':
                self.distances[current_pos, current_dir] = float('inf')
                continue
            if current_pos == self.end and current_distance <= self.shortest_route:
                self.shortest_route = current_distance
                self.best_route.update(current_route)
                continue
            for next_dir in directions:
                pos: tuple = (x+next_dir[0], y+next_dir[1])
                x_next, y_next = pos
                if x_next < 0 or x_next >= self.width or y_next < 0 or y_next >= self.height:
                    continue
                if current_dir == next_dir:
                    distance: int = current_distance + self.move
                elif current_dir == (-next_dir[0], -next_dir[1]):
                    distance: int = current_distance + 2*self.turn + self.move
                else:
                    distance: int = current_distance + self.turn + self.move
                if distance <= self.distances[pos, next_dir]+self.turn:
                    self.distances[pos, next_dir] = distance
                    heapq.heappush(priority_queue, (distance, pos, next_dir, current_route + [pos]))
        if verbose:
            for y in range(self.height):
                for x in range(self.width):
                    dist = min(map(lambda d: self.distances[((x, y), d)], ((1, 0), (0, -1), (-1, 0), (0, 1))))
                    print(f"{dist}".center(6), end='')
                print()
            print()
        return self.shortest_route, self.best_route#self.distances[self.end]

    def make_paths(self) -> None:
        for p in self.best_route:
            x, y = p
            if not (x, y) in (self.start, self.end):
                self.map[y][x] = 'O'
        return

    def reset_paths(self) -> None:
        self.map = list(list(map(lambda x: '.' if x == 'O' else x, self.map[i])) for i in range(len(self.map)))
        return

    def print_map(self) -> None:
        for line in self.map:
            for _ in line:
                if _ == '#':
                    print(Fore.RED + Style.DIM + _, end='')
                elif _ == 'S':
                    print(Fore.WHITE + Style.BRIGHT + _, end='')
                elif _ == 'E':
                    print(Fore.GREEN + Style.BRIGHT + _, end='')
                elif _ == 'O':
                    print(Fore.YELLOW + Style.BRIGHT + _, end='')
                else:
                    print(Fore.WHITE + Style.DIM + _, end='')
            print()
        print()
        return


def pathfinder(text, part=1, verbose=False) -> int:
    # identify global variables
    global map_
    global searched
    global paths
    global north
    global south
    global east
    global west
    global i_end
    # reset global variables
    del map_
    del searched
    searched = {}
    del paths
    paths = []
    del i_end
    # set local variables
    map_ = text.strip('\n').split('\n')
    width, height = text.index('\n'), text.count('\n')
    print(f"Dimension: {width} x {height}")
    start: int = text.index('S')
    i_start: tuple = (start % (width+1), start // (width+1))
    end: int = text.index('E')
    i_end = (end % (width+1), end // (width+1))
    print(f"start: {i_start}\n  end: {i_end}")

    dijk: Dijkstra = Dijkstra(map_, i_start, i_end, move=1, turn=1000)
    total: tuple = dijk.find_shortest_path(east)
    dijk.make_paths()
    #dijk.reset_paths()
    dijk.print_map()
    if part == 2:
        return len(total[1])
    return total[0]


def run_test(text, test_inputs=[('', 0)], part=1) -> None:
    res: int = pathfinder(test_inputs[0][0], part=part, verbose=True)
    print()
    if res == test_inputs[0][1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!\n\n")
        if len(test_inputs) > 1:
            res: int = pathfinder(test_inputs[1][0], part=part, verbose=True)
            print()
            if res == test_inputs[1][1]:
                if len(test_inputs) > 2:
                    res: int = pathfinder(test_inputs[2][0], part=part, verbose=True)
                    if res == test_inputs[2][1]:
                        print(Fore.GREEN + "All tests passed\n\n")
        res: int = pathfinder(text, part=part, verbose=False)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
    print()
    print("Part " + 'I'*part + ": " + Style.BRIGHT + f"{res}\n\n")


if __name__ == "__main__": # 7036  11048
    run_test(input_16, [(input_test, 7036), (input_test_2, 11048), (input_test_3, 4013)], part=1)
    print('\n' + '='*10 + '\n')
    run_test(input_16, [(input_test, 45), (input_test_2, 64), (input_test_3, 14)], part=2)
    
