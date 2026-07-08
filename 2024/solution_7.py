input_test1: list = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".split('\n')

input_7: list = open("input_7").readlines()

def operator(target, num, nums, mode=1) -> bool:
    if len(nums) == 0:
        return target == num

    res_add: int = num + nums[0]
    res_mul: int = num * nums[0]
    res_cat: int = int(f"{num}{nums[0]}")

    result = operator(target, res_add, nums[1:], mode) \
            or operator(target, res_mul, nums[1:], mode)

    if mode == 1:
        return result
    if mode == 2:
        return result or operator(target, res_cat, nums[1:], mode)
    else:
        raise ValueError("mode must be set to 1 (add, mul) or 2 (add, mul, cat)")

def solve(lines, mode=1, verbose=False) -> int:
    if lines[0] == '':
        lines.remove('')
        lines.remove('')
    operations: list = [[int(line.split(': ')[0]), list(map(int, line.split(': ')[1].split()))] for line in lines]
    result = 0
    for n, operation in enumerate(operations):
        if verbose:
            print(lines[n])
        valid: bool = operator(operation[0], operation[1][0], operation[1][1:], mode=mode)
        if valid:
            if verbose:
                print("  - Valid!")
            result += operation[0]
    if verbose:
        print()
        print(result)
    return result


if solve(input_test1, mode=1) == 3749:
    print('-'*20)
    r: int = solve(input_7, mode=1)
    print('='*20)
    print(f"Part I: {r}")

if solve(input_test1, mode=2) == 11387:
    print('-'*20)
    r: int = solve(input_7, mode=2)
    print('='*20)
    print(f"Part II: {r}")
