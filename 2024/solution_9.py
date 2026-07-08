from colorama import init, Fore, Style
from copy import deepcopy
from pprint import pprint

init(autoreset=True)

input_test = \
"""2333133121414131402""".split('\n')

input_9 = open("input_9").readlines()
test_9 = open("test_9").readlines()  #63614979355824|97898222299196

def defragment(lines, mode=1, test=0, verbose=False) -> int:
    coded_disk = ''.join(lines).replace('\n', '')
    total: int = 0
    if test == 0:
        disk: list = create_disk(coded_disk)
        print("Disk created...")
        disk_defrag: list = shift(disk, mode=mode, verbose=verbose)
    else:
        disk_defrag: list = shift(coded_disk, mode=mode, test=test, verbose=verbose)
    if verbose:
        print(disk_defrag)
    print("Disk defragmented...")
    total: int = checksum(disk_defrag)
    if verbose:
        print(f"checksum: {total}")
    return total

def create_disk(code) -> list:
    disk = []
    for i in range(0, len(code)//2+1):
        for _ in range(int(code[2*i])):
            d = str(int(i))
            disk.append(d)
        if 2*i >= (len(code)-1):
            continue
        for _ in range(int(code[2*i+1])):
            disk.append('.')
    return disk

def encrypt_disk(disk) -> str:
    o: list = []
    s: str = ''
    for i in range(len(disk)):
        j: int = 0
        if (not disk[i+j].isdigit()) or disk[i+j]==s:
            continue
        s: str = disk[i+j]
        try:
            while disk[i+j+1] == s:
                j += 1
                if i+j+1 == len(disk):
                    break
        except IndexError:
            print()
            print(i, j)
            raise Exception
        o.append(j+1)
        print(o[-1], end='')
        #j += 1
        if i+j+1 == len(disk):
            continue
        k = 0
        while disk[i+j+k+1] == '.':
            k += 1
            if (i+j+k+1) == len(disk):
                break
        o.append(k)
        print(o[-1], end='')
    print()
    return ''.join(map(str, o))

def shift(disk, mode=1, test=0, verbose=False) -> list:
    if mode == 1:
        for i in range(len(disk)):
            if disk[i].isdigit():
                continue
            for j in range(len(disk)-1, 0, -1):
                if j < i:
                    return disk
                if not disk[j].isdigit():
                    continue
                disk[i] = deepcopy(disk[j])
                disk[j] = '.'
                break
            if verbose:
                print(''.join(disk))
    elif test == 0:
        #print(max(disk))
        file_dict: dict = find_files(disk)
        print("files found")
        files: list = sorted(file_dict.keys(), reverse=True)#list(file_dict.keys())#
        #print(files)
        #pprint(file_dict)
        if verbose:
            print(find_gaps(disk))
        # while len(files) > 1:
        #     f = max(files)
        gaps: dict = find_gaps(disk)
        for f in files:
            if verbose:
                print(''.join(disk))
            #pprint(gaps)
            #for g in filter(lambda x: x < file_dict[f]["idx"], sorted(gaps.keys())):
            for g in filter(lambda x: x < file_dict[f]["idx"], gaps.keys()):#range(file_dict[f]["idx"]):
                j: int = 0
                #if disk[g].isdigit():
                #    continue
                #while not disk[g+j+1].isdigit():
                #    j += 1
                #    if g+j+1 == len(disk):
                #        break
                if (gaps[g] >= file_dict[f]["size"]):
                #print(g, j+1)
                #if (j+1) >= file_dict[f]["size"]:
                    for _ in range(file_dict[f]["size"]):
                        disk[g+_] = f
                        disk[file_dict[f]["idx"]+_] = '.'
                    gaps[g+file_dict[f]["size"]] = gaps[g] - file_dict[f]["size"]
                    # gaps[g] -= file_dict[f]["size"]
                    del gaps[g]
                    break
            # files.remove(f)
    else:
        files: list = []
        gaps_: list = []
        idx: int = 0
        for i, _ in enumerate(disk):
            if i % 2:
                gaps_.append([deepcopy(idx), int(_)])
            else:
                files.append([deepcopy(idx), int(_), i//2])
            idx += int(_)
        #print(files)
        print("Files analysed...")
        for n in range(len(files)-1, -1, -1):
            for m in range(len(gaps_)):
                if gaps_[m][1] >= files[n][1] and gaps_[m][0] < files[n][0]:
                    i_temp = files[n][0]
                    files[n][0] = gaps_[m][0]
                    gaps_[m][0] += files[n][1]
                    gaps_[m][1] -= files[n][1]
                    gaps_.append([i_temp, files[n][1]])
                    break
        temp_disk = deepcopy(disk)
        temp_files: list = sorted(files + gaps_, key=lambda x: x[0])
        #print(temp_files)
        print("Making disk")
        disk = []
        for i in range(len(temp_files)):
            for _ in range(temp_files[i][1]):
                if len(temp_files[i]) > 2:
                    disk.append(temp_files[i][2])
                else:
                    disk.append('.')
            #if i+1 == len(temp_files):
            #    continue
            #for _ in range(gaps_[i][1]):
            #    disk.append('.')
        if verbose:
            print(''.join(map(str, disk)))
    return disk

def find_gaps(disk):
    gaps = {}
    g = 0
    for i in range(len(disk)):
        if (not disk[i].isdigit()) and (i >= g):
            g = deepcopy(i)
            j = 0
            while not disk[i+j+1].isdigit():
                j += 1
                if i+j+1 == len(disk):
                    break
            gaps[i] = j+1
            g += j+1
    return gaps

def find_files(disk):
    files = set(disk) - set('.')
    #print(files)
    files_dict = {}
    for f in list(files):
        files_dict[f] = {"size": disk.count(f), "idx": disk.index(f)}
    return files_dict

def checksum(disk, files=None) -> int:
    #print(''.join(disk))
    cs: int = 0
    for i in range(len(disk)):
        if disk[i] == '.':
            continue
        #print(i, disk[i])
        if files:
            cs += files[i]*int(disk[i])
        else:
            cs += i*int(disk[i])
    return cs


if __name__ == "__main__":
    mode: int = 2
    test: int = 1
    res: int = defragment(input_test, mode=mode, test=test, verbose=True)
    if res == 1928:
        print(Fore.GREEN + f"Part I passed!")
        res = defragment(test_9)
        print(f"Part I: {res}")
        if res == 63614979355824:
            print(Fore.GREEN + "- Part I second test passed")
            res = defragment(input_9, mode=2)
        else:
            print(Fore.RED + "- Part I second test failed")
    if res == 2858:
        print(Fore.GREEN + "Part II passed!!")
        res = defragment(test_9, mode=2, test=test)
        if res == 97898222299196:
            print(Fore.GREEN + "- Part II second test passed")
            res = defragment(input_9, mode=2, test=test)
        else:
            print(Fore.RED + "- Part II second test failed")
        print(f"Part II: {res}")
    print(encrypt_disk(create_disk(''.join(input_test).replace('\n', ''))))
