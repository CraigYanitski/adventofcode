from colorama import init, Fore, Style
from pprint import pprint
from functools import lru_cache

init(autoreset=True)

test1 = \
"""OOOOO
   OXOXO
   OOOOO
   OXOXO
   OOOOO
""".replace('   ', '')

test2 = \
"""AAAA
   BBCD
   BBCC
   EEEC
""".replace('   ', '')

test3 = \
"""EEEEE
   EXXXX
   EEEEE
   EXXXX
   EEEEE
""".replace('   ', '')

test4 = \
"""AAAAAA
   AAABBA
   AAABBA
   ABBAAA
   ABBAAA
   AAAAAA
""".replace('   ', '')

input_test: str = \
"""RRRRIICCFF
   RRRRIICCCF
   VVRRRCCFFF
   VVRCCCJFFF
   VVVVCJJCFE
   VVIVCCJJEE
   VVIIICJJEE
   MIIIIIJJEE
   MIIISIJEEE
   MMMISSJEEE
""".replace('   ', '')

input_12 = open("input_12").read()

plot_dict = {}

def print_dict():
    global plot_dict
    for k in plot_dict.keys():
        for i in range(len(plot_dict[k]["points"])):
            print(f"Plot {k}: area = {plot_dict[k]['area'][i]}; perimeter = {plot_dict[k]['perimeter'][i]}; price = {plot_dict[k]['price'][i]}")

def calculate_price(text, side=False, verbose=False) -> int:
    width = text.index('\n')
    height = text.count('\n')
    print(width, height)
    print('-'*10)
    map_ = text.split('\n')[:-1]
    if len(map_) != height:
        raise Exception(Fore.RED + "Data improperly read")
    total = 0
    global plot_dict
    plot_dict = {}
    for y in range(height):
        for x in range(width):
            search = True
            #idx = 0
            target = map_[y][x]
            if target in plot_dict.keys():
                for plot_p in plot_dict[target]["points"]:
                    if (x, y) in plot_p:
                        search = False
                if not search:
                    continue
                p_idx = len(plot_dict[target]["points"])
                plot_dict[target]["points"].append([])
                plot_dict[target]["area"].append(0)
                plot_dict[target]["perimeter"].append(0)
                plot_dict[target]["price"].append(0)
            else:
                p_idx = 0
                plot_dict[target] = {}
                plot_dict[target]["points"] = [[]]
                plot_dict[target]["area"] = [0]
                plot_dict[target]["perimeter"] = [0]
                plot_dict[target]["price"] = [0]
            same_plot(map_, (x, y), target, p_idx, setup=True)
    for k in plot_dict.keys():
        i_max = len(plot_dict[k]["points"])
        for i in range(i_max):
            area = len(plot_dict[k]["points"][i])
            plot_dict[k]["area"][i] = area
            peri= sum(map(lambda p: perimeter(map_, p, k, side=side), set(plot_dict[k]["points"][i])))
            plot_dict[k]["perimeter"][i] = peri
            plot_dict[k]["price"][i] = area * peri
            total += area * peri
    if verbose:
        print_dict()
    return total

def same_plot(map_, pos, target, idx=0, setup=False, oob=False) -> bool:
    x, y, = pos
    width = len(map_[0])
    height = len(map_)
    global plot_dict
    if setup:
        if 0 <= x < width and 0 <= y < height:
            if map_[y][x] == target and not (x, y) in plot_dict[target]["points"][idx]:
                plot_dict[target]["points"][idx].append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    same_plot(map_, (pos[0]+dx, pos[1]+dy), target, idx, setup=True)
    else:
        if 0 <= x < width and 0 <= y < height:
            if map_[y][x] == target:
                return True
            else:
                return oob
        else:
            return False
    return False

def perimeter(map_, pos, target, side=False) -> int:
    x, y = pos
    if side:
        c: int = 0
        for dx, dy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            corner: bool = ((not same_plot(map_, (x+dx, y+dy), target, oob=False)) 
                             and (   same_plot(map_, (x+dx, y+0 ), target, oob=False) 
                                  == same_plot(map_, (x+0 , y+dy), target, oob=False)))
            corner2 = ((same_plot(map_, (x+dx, y+dy), target, oob=False)) 
                             and not (   same_plot(map_, (x+dx, y+0 ), target, oob=False)
                                      or same_plot(map_, (x+0 , y+dy), target, oob=False)))
            if corner or corner2:
                c += 1
        return c
    else:
        p: int = 0
        for dx, dy in ((1, 0), (-1, 0), (0, 1),(0, -1)):
            if same_plot(map_, (x+dx, y+dy), target):
                pass
            else:
                p += 1
        return p


if __name__ == "__main__":
    res = calculate_price(input_test, verbose=True)
    if res == 1930:
        print(Fore.GREEN + "Part I passed!")
        print()
        if calculate_price(test1, verbose=True) == 772:
            if calculate_price(test2, verbose=True) == 140:
                res = calculate_price(input_12)
    else:
        print(Fore.RED + "Part I failed...")
        exit()
    print()
    print(f"Part I: {res}")
    print('=' * 10)
    res = calculate_price(test2, side=True, verbose=True)
    if res == 80:
        print(Fore.GREEN + "Part II passed!")
        if calculate_price(test1, side=True, verbose=True) == 436:
            if calculate_price(input_test, side=True, verbose=True) == 1206:
                if calculate_price(test3, side=True, verbose=True) == 236:
                    if calculate_price(test4, side=True, verbose=True) == 368:
                        print(Fore.GREEN + "All tests passed!")
                        res = calculate_price(input_12, side=True)
    else:
        print(Fore.RED + "Part II failed...")
    print()
    print(f"Part II: {res}")

