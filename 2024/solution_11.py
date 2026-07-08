from colorama import init, Fore, Style
from pprint import pprint
from collections import deque
from functools import lru_cache, partial
from copy import deepcopy

init(autoreset=True)

input_test: str = \
"""125 17""".replace('   ', '')

input_11: str = open("input_11").read()

def print_line(line) -> None:
    # line = list(map(str, line))
    for _ in line:
        if isinstance(_, map):
            print_line(list(_))
        elif _ == 0:
            print(Fore.CYAN + str(_), end=' ')
        elif _ == 1:
            print(Fore.BLUE + str(_), end=' ')
        elif (len(str(_)) % 2) == 0:
            print(Fore.LIGHTGREEN_EX + str(_), end=' ')
        else:
            print(Fore.MAGENTA + str(_), end=' ')
    # print()
    return

def stones(text, blinks=25, verbose=False) -> int:
    line: list = list(map(int, text.replace('\n', '').split()))
    #for _ in range(blinks):
    #    if verbose:
    #        print_line(line)
    #    i_shift: int = 0
    new_line: map = map(partial(apply_rules, blink=0, max_iter=blinks), line)
    #    for i in range(len(line)):
    #        vals: list = apply_rules(line[i+i_shift])
    #        if len(vals) == 2:
    #            line[i+i_shift] = vals[1]
    #            line.insert(i+i_shift, vals[0])
    #            i_shift += 1
    #        else:
    #            line[i+i_shift] = vals[0]
    #    if blinks > 25:
    #        print(f"{_+1}: {len(line)}")
    if verbose:
        print_line(deepcopy(new_line))
        print()
    #total: int = nested_count(new_line.copy())
    return sum(list(new_line))#nested_count(new_line)

def nested_count(m) -> int:
    c: int = 0
    for _ in m:
        if isinstance(_, map):
            c += nested_count(_)
        #elif isinstance(_, list):
        #    c += len(_)
        elif isinstance(_, int):
            c += 1
        else:
            #c += 10
            print(c)
    return c

@lru_cache(maxsize=None)
def apply_rules(val, blink=1, max_iter=25) -> int:
    if blink == max_iter:
        return 1#val
    if val == 0:
        return apply_rules(1, blink=blink+1, max_iter=max_iter)
    elif (len(str(val)) % 2) == 0:
        sv: str = str(val)
        ih: int = len(sv)//2
        m = map(partial(apply_rules, blink=blink+1, max_iter=max_iter), [int(sv[:ih]), int(sv[ih:])])
        return sum(list(m))
    else:
        return apply_rules(2024*val, blink=blink+1, max_iter=max_iter)


if __name__ == "__main__":
    res: int = stones(input_test, blinks=6, verbose=True)
    if res == 22:
        res = stones(input_test, blinks=25)
        if res == 55312:
            print(Fore.GREEN + "Part I test passed!!!")
            res = stones(input_11, blinks=25)
        else:
            print(Fore.RED + "Part I test failed...")
    print(f"Part I: {res}")
    print()
    res: int = stones(input_11, blinks=75)
    print(Fore.GREEN + "Part II finished evaluating...")
    print(f"Part II: {res}")
    print()
    print(f"Cache used: {apply_rules.cache_info()}")
    print()

