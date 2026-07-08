import time

input_test: list[str] = """MMMSXXMASM
                           MSAMXMSMSA
                           AMXSXMAAMM
                           MSAMASMSMX
                           XMASAMXAMM
                           XXAMMXXAMA
                           SMSMSASXSS
                           SAXAMASAAA
                           MAMMMXMMMM
                           MXMXAXMASX""".split()
input_test2: list[str] = """.M.S......
                            ..A..MSMS.
                            .M.S.MAA..
                            ..A.ASMSM.
                            .M.S.M....
                            ..........
                            S.S.S.S.S.
                            .A.A.A.A..
                            M.M.M.M.M.
                            ..........""".split()

input_4: list[str] = open('input_4').readlines()

time_s = time.time()

puzzle: list[str] = input_4
height: int = len(puzzle)
width: int = len(puzzle[0])
total1: int = 0
total2: int = 0

for i, line in enumerate(puzzle):
    for j, _ in enumerate(line):
        if _ == 'X':
            if i >= 3:
                if (puzzle[i][j]
                    + puzzle[i-1][j]
                    + puzzle[i-2][j]
                    + puzzle[i-3][j]) in ("XMAS", "SAMX"):
                    total1 += 1
            if i <= height-4:
                if (puzzle[i][j]
                    + puzzle[i+1][j]
                    + puzzle[i+2][j]
                    + puzzle[i+3][j]) in ("XMAS", "SAMX"):
                    total1 += 1
            if j >= 3:
                if puzzle[i].endswith("SAMX", 0, j+1):
                    total1 += 1
                if i >= 3:
                    if (puzzle[i][j]
                        + puzzle[i-1][j-1]
                        + puzzle[i-2][j-2]
                        + puzzle[i-3][j-3]) in ("XMAS", "SAMX"):
                        total1 += 1
                if i <= height-4:
                    if (puzzle[i][j]
                        + puzzle[i+1][j-1]
                        + puzzle[i+2][j-2]
                        + puzzle[i+3][j-3]) in ("XMAS", "SAMX"):
                        total1 += 1
            if j <= width-4:
                if puzzle[i].startswith("XMAS", j):
                    total1 += 1
                if i >= 3:
                    if (puzzle[i][j]
                        + puzzle[i-1][j+1]
                        + puzzle[i-2][j+2]
                        + puzzle[i-3][j+3]) in ("XMAS", "SAMX"):
                        total1 += 1
                if i <= height-4:
                    if (puzzle[i][j]
                        + puzzle[i+1][j+1]
                        + puzzle[i+2][j+2]
                        + puzzle[i+3][j+3]) in ("XMAS", "SAMX"):
                        total1 += 1
        if _ == 'A':
            if 1 <= i <= height-2 and 1 <= j <= width-2:
                if (    (puzzle[i-1][j-1]+puzzle[i+1][j+1] in ['MS', 'SM'])
                    and (puzzle[i-1][j+1]+puzzle[i+1][j-1] in ['MS', 'SM'])):
                    total2 += 1
        else:
            pass


print(total1)
print(total2)

time_1 = time.time()
print(time_1 - time_s)


def get_indeces(pattern, ref=0, ex=False):
    indeces = [i-ref for i in range(len(pattern))]
    if ex:
        indeces.remove(indeces[ref])
    return indeces

def get_coordinates(origin, pattern, ref=0, mode="right", wrap=False, ex=False):
    indeces = get_indeces(pattern, ref, ex=ex)
    coordinates = []
    for i in indeces:
        if mode == "right":
            dx, dy = 0, i
        elif mode == "left":
            dx, dy = 0, -i
        elif mode == "down":
            dx, dy = i, 0
        elif mode == "up":
            dx, dy = -i, 0
        elif mode == "downright":
            dx, dy = i, i
        elif mode == "upright":
            dx, dy = i, -i
        elif mode == "downleft":
            dx, dy = -i, i
        elif mode == "upleft":
            dx, dy = -i, -i
        else:
            dx, dy = 0, 0
        if not wrap and ((origin[0]+dy < 0) or (origin[1]+dx < 0)):
            return []
        coordinates.append((origin[0]+dy, origin[1]+dx))
    return coordinates

def find_patterns(grid, pattern, ref=0):
    start: int = 0
    height: int = len(grid)
    width: int = len(grid[0])
    count: int = 0
    #print('-', pattern)
    #print('-', pattern[::-1])
    for i in range(start, height):
        for j in range(start, width):
            if grid[i][j] == pattern[ref]:
                for mode in ["right", 
                             "left",
                             "up",
                             "down",
                             "downright",
                             "downleft",
                             "upright",
                             "upleft"]:
                    coordinates: list[tuple[int]] = get_coordinates((i, j), pattern, ref, mode=mode)
                    try:
                        if (''.join([grid[i][j] for i, j in coordinates]) in [pattern, pattern[::-1]]):
                            #print(''.join([grid[i][j] for i,j in coordinates]))
                            count += 1
                    except:
                        pass
    return count

def find_x(grid, pattern, ref=1):
    height: int = len(grid)
    width: int = len(grid[0])
    count: int = 0
    new_pattern = pattern[:ref]+pattern[ref+1:]
    #print(f"  {new_pattern}")
    for i in range(ref, height-ref):
        for j in range(ref, width-ref):
            if grid[i][j] == pattern[ref]:
                coor1: list[tuple[int]] = get_coordinates((i, j), pattern, ref, 
                                                          mode="downright", ex=True)
                coor2: list[tuple[int]] = get_coordinates((i, j), pattern, ref, 
                                                          mode="downleft", ex=True)
                #print(f"  {''.join([grid[i][j] for i, j in coor1])}")
                if ((''.join([grid[i][j] for i, j in coor1]) in [new_pattern, new_pattern[::-1]])
                    and (''.join([grid[i][j] for i, j in coor2]) in [new_pattern, new_pattern[::-1]])):
                    count += 1
    return count

time_i = time.time()
print(f"Part I: {find_patterns(input_4, 'XMAS')}")
time_2 = time.time()
print(time_2 - time_i)
print(f"Part II: {find_x(input_4, 'MAS', ref=1)}")
time_3 = time.time()
print(time_3 - time_2)
time_e = time.time()-time_s
print(time_e)

