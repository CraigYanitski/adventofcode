from colorama import init, Fore, Style
from functools import lru_cache

init(autoreset=True)

input_test: str = \
"""89010123
   78121874
   87430965
   96549874
   45678903
   32019012
   01329801
   10456732
""".replace('   ', '')

input_10: str = open("input_10").read()

def print_map(text) -> None:
    '''
    A function to print the map, highlighting bases and peaks.
    '''
    print()
    for _ in text:
        if _ == '0':
            print(Fore.CYAN + Style.BRIGHT + _, end='')
        elif _ == '9':
            print(Fore.GREEN + Style.BRIGHT + _, end='')
        # elif _ == '\n':
        #     print("new line")
        else:
            print(Fore.LIGHTBLACK_EX + Style.DIM + _, end='')
    print()
    return

def hiking(text: str, part=1, base='0', peak='9', verbose=False, test=False) -> int:
    '''
    A function to search map for unique paths from the lowest locations (trailheads) 
    to the highest locations (peaks).
    It returns the sum of each trailhead's score.

    - part 1: the trailhead score is the number of unique peaks that can be reached 
      by a valid path.

    - part 2: the trailhead score is the number of unique paths that end in a peak.
    '''
    # initialise map-relevant variables
    peaks: list = []
    total: int = 0
    width: int = text.index('\n')
    height: int = text.count('\n')

    # clean new lines from map
    map_: str = text.replace('\n', '')
    print_map(text)

    # debug printing
    if verbose:
        print(f"width {width}, height {height}")
        print()

    # initialise coordinate increments
    dx, dy = 1, 1

    # loop through rows to find trailheads
    for y in range(height):
        # extract row
        i: int = 0
        line: str = map_[y*height:y*height+width]

        # check for trailhead in row
        while base in line[i:]:
            # locate trailhead
            x: int = line[i:].index(base)

            # build list of peaks reachable from trailhead
            t: list = []
            t += pathfinding(map_, (i+x, y), (i+x+dx, y   ), (width, height), peak=peak, test=False)
            t += pathfinding(map_, (i+x, y), (i+x-dx, y   ), (width, height), peak=peak, test=False)
            t += pathfinding(map_, (i+x, y), (i+x   , y+dy), (width, height), peak=peak, test=False)
            t += pathfinding(map_, (i+x, y), (i+x   , y-dy), (width, height), peak=peak, test=False)

            # update map-relevant variables
            peaks += t
            peaks = list(set(peaks))
            if part == 2:
                total += len(t)
            else:
                total += len(set(t))

            # debug printing
            if verbose:
                print(f"({i+x}, {y}) path total: {len(set(t))}")
                print(set(t))

            # update horizontal index to just after previous trailhead
            i += x+1

            # break if debugging
            if test or i == width:
                break
        # break if debugging
        if test:
            break

    # return total
    return total

@lru_cache(maxsize=None)
def pathfinding(map_, current, next_, dim, inc=1, peak='9', test=False) -> list:
    '''
    A function to recursively identify the valid path(s).
    It returns a list of the peak indices reached, with 
    length of the unique paths.
    '''
    # Extract current and next indices
    xc, yc = current
    xn, yn = next_

    # debug printing
    if test:
        print(current, next_)
        print(map_[yc*dim[1]+xc], end=' ')

    # Check if the next coordinate is valid.
    if ((0 <= next_[0] < dim[0]) and (0 <= next_[1] < dim[1])):
        # debug printing
        if test:
            print(map_[yn*dim[1]+xn])

        # Check if path is valid
        if int(map_[yn*dim[1]+xn]) - int(map_[yc*dim[1]+xc]) != inc:
            # debug printing
            if test:
                print("impassable...")
                print()

            # return empty list if the next coordinates are invalid
            return []

        # Check if peak is reached
        if map_[yn*dim[1]+xn] == peak:
            # debug printing
            if test:
                print(Fore.GREEN + "path found!!")
                print()

            # return list containing tuple of coordinates
            return [(xn, yn)]

        # compute direction
        dx, dy = next_[0]-current[0], next_[1]-current[1]

        # debug printing
        if test:
            print(dx, dy)
        #current = next_

        # return sum of next of next coordinates, not including next coordinates
        if dx:
            dy: int = 1
            t: list = (  pathfinding(map_, (xn, yn), (xn+dx, yn   ), dim, test=test)
                       + pathfinding(map_, (xn, yn), (xn   , yn+dy), dim, test=test)
                       + pathfinding(map_, (xn, yn), (xn   , yn-dy), dim, test=test))

            # debug printing
            if test:
                print(t)
            return t
        elif dy:
            dx: int = 1
            t: list = (  pathfinding(map_, (xn, yn), (xn   , yn+dy), dim, test=test)
                       + pathfinding(map_, (xn, yn), (xn+dx, yn   ), dim, test=test)
                       + pathfinding(map_, (xn, yn), (xn-dx, yn   ), dim, test=test))
            
            # debug printing
            if test:
                print(t)
            return t
    # debug printing
    if test:
        print()
        print("out of bounds...")
        print()

    # return empty list if not a valid coordinate
    return []


if __name__ == "__main__":
    # check test input for Part I
    res: int = hiking(input_test, verbose=True, test=False)
    if res == 36:
        print(Fore.GREEN + "Part I test passed!")
        res = hiking(input_10)
    else:
        print(Fore.RED + "Part I test failed :-(")
    print(f"\nPart I: {res}")
    print()

    # Check test input for Part II
    res: int = hiking(input_test, part=2, verbose=True, test=False)
    if res == 81:
        print(Fore.GREEN + "Part II test passed!")
        res = hiking(input_10, part=2)
    else:
        print(Fore.RED + "Part II test failed :-(")
    print(f"\nPart II: {res}")
