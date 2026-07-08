from colorama import init, Fore, Style

init(autoreset=True)

input_test1: list[str] = \
        """47|53
           97|13
           97|61
           97|47
           75|29
           61|13
           75|53
           29|13
           97|29
           53|29
           61|53
           97|53
           61|29
           47|13
           75|47
           97|75
           47|61
           75|61
           47|29
           75|13
           53|13

           75,47,61,53,29
           97,61,53,29,13
           75,29,13
           75,97,47,61,53
           61,13,29
           97,13,75,29,47""".replace(' ', '').split("\n\n")

input_5: list[str] = open("input_5").read().replace(' ', '').split("\n\n")
#print(input_5)

def check_validity(pages, rules) -> tuple[bool,list[list[int]]]:
    good: bool = True
    wrong_pages: dict = {}
    relevant_rules: list[list[int]] = []
    for rule in rules:
        order: list[int] = list(map(int, rule.split('|')))
        if (order[0] in pages) and (order[1] in pages):
            relevant_rules.append('|'.join([str(o) for o in order]))
            if pages.index(order[1]) > pages.index(order[0]):
                pass
            else:
                good = False
                #break
                wrong_pages[rule] = order
        else:
            pass
    #reordered = pages
    #if not good:
    #else:
    #    pass
    return good, relevant_rules

def reorder_line(pages, rules):
    while not check_validity(pages, rules)[0]:
        # print('-', pages)
        for rule in rules:
            order = list(map(int, rule.split('|')))
            # print('-', rule)
            i1, i2 = pages.index(order[0]), pages.index(order[1])
            if i1 > i2:
                pages[i1] = order[1]
                pages[i2] = order[0]
            else:
                pass
    return pages

def test(inp) -> int:
    rules, updates = [i.split() for i in inp]
    #print(len(rules))
    #res = input("proceed? ")
    #if res in 'yY':
    #    pass
    #else:
    #    return
    print()
    correct: list[str] = []
    wrong: list[str] = []
    total: int = 0
    total2: int = 0
    print("-"*5 + "valid updates" + "-"*5)
    for update in updates:
        pages: list[int] = list(map(int, update.split(',')))
        good, relevant_rules = check_validity(pages, rules)
        new_update = reorder_line(pages, relevant_rules)
        if good:
            print(Style.BRIGHT+Fore.GREEN+update)
            correct.append(update)
            total += pages[len(pages)//2]
            if not (len(pages) % 2):
                print("<<Even number in valid update!!>>")
        else:
            print(f"{Style.BRIGHT+Fore.RED}    {','.join(str(i) for i in new_update)}")
            wrong.append(new_update)
            total2 += new_update[len(new_update)//2]
    print("-"*23)
    print()
    return total, total2

if test(input_test1) == (143, 123):
    print("="*6 + " PASS " + "="*6)
    print()
    print(f"Part I, II: {test(input_5)}")
else:
    print("="*6 + " FAIL " + "="*6)
    raise Exception("Code doest not pass example!!")
