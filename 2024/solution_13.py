from re import A
from colorama import init, Fore, Style
from pprint import pprint

init(autoreset=True)

input_test: str = \
"""Button A: X+94, Y+34
   Button B: X+22, Y+67
   Prize: X=8400, Y=5400
   
   Button A: X+26, Y+66
   Button B: X+67, Y+21
   Prize: X=12748, Y=12176
   
   Button A: X+17, Y+86
   Button B: X+84, Y+37
   Prize: X=7870, Y=6450
   
   Button A: X+69, Y+23
   Button B: X+27, Y+71
   Prize: X=18641, Y=10279
""".replace('   ', '')

input_13: str = open("input_13").read()


def claw_game(text: str, part=1, verbose=False) -> int:
    if text == '':
        return 0
    total: int = 0
    games: list = text[:-1].split("\n\n")
    for i, game in enumerate(games):
        if verbose:
            print(game)
        a, b, p     = list(map(lambda x: x.split(': ')[1], game.split('\n')[:3]))
        A, B, prize = list(map(lambda x: list(map(lambda z: int(z[2:]), x)), map(lambda y: y.split(', '), (a, b, p))))
        if part == 2:
            prize = (1e13+prize[0], 1e13+prize[1])
        moves: int = solve_game(A, B, prize, price=(3, 1), opt=True, verbose=verbose)
        total += moves
    return total

def solve_game(a, b, loc, price=(1, 1), opt=True, verbose=False) -> int:
    ax, ay = a
    bx, by = b
    px ,  py = loc
    ta ,  tb = price
    if verbose:
        print(f"A  {a};  B  {b};  prize  {loc}")
    moves = 0
    pos = play_game(a, b, 100, 100)
    if opt:
        det_aa: int = (px*by-py*bx)
        det_ab: int = (ax*py-ay*px)
        det_a: int = (ax*by-ay*bx)
        if verbose:
            print(det_aa, det_ab, det_a)
        # if det_aa < 0 or det_ab < 0 or det_a < 0:
        #     if verbose:
        #         print(f"A: {None}, B: {None}, price: {None}")
        #         print()
        #     return 0
        n_a: float = det_aa / det_a
        n_b: float = det_ab / det_a
        if (n_a % 1) or (n_b % 1):
            if verbose:
                print(f"A: {None}, B: {None}, price: {None}")
                print()
            return 0
        moves: int = ta*int(n_a) + tb*int(n_b)
        if verbose:
            print(f"A: {n_a}, B: {n_b}, price: {moves}")
    else:
        if pos[0] < px and pos[1] < py:
            if verbose:
                print(f"A: {None}, B: {None}, price: {None}")
                print()
            return 0
        for n_a in range(101):
            for n_b in range(101):
                if win_game(a, b, n_a, n_b, loc):
                    moves: int = ta*n_a + tb*n_b
                    if verbose:
                        print(f"A: {n_a}, B: {n_b}, price: {moves}")
                    break
            if moves > 0:
                break
    if verbose:
        print()
    return moves

def win_game(a, b, n_a, n_b, p) -> bool:
    pos: tuple = play_game(a, b, n_a, n_b)
    win: bool = all((p[0]==pos[0], p[1]==pos[1]))
    return win

def play_game(a, b, n_a, n_b) -> tuple:
    dxa, dya = a
    dxb, dyb = b
    pos = (dxa*n_a + dxb*n_b, dya*n_a + dyb*n_b)
    return pos

def run_tests(text, tests=('', 0), part=1) -> None:
    #if part == 2 and tests[0] == '':
    #    tests = 
    res: int = claw_game(tests[0], verbose=True)
    if res == tests[1]:
        print(Fore.GREEN + "Part " + part*'I' + " test passed!!")
        res = claw_game(text, part=part)
    else:
        print(Fore.RED + "Part " + part*'I' + " test failed...")
    print()
    print("Part " + part*'I' + f": {res}")
    return


if __name__ == "__main__":
    run_tests(input_13, (input_test, 480))
    print('=' * 10)
    run_tests(input_13, part=2)

