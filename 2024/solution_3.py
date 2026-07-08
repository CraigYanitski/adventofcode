import re

input_test1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
input_test2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
input_3 = open("input_3").read()

commands = input_3

total = 0
do = True

for i,_ in enumerate(commands):
    if _ != 'm':
        if _ != 'd':
            pass
        else:
            if commands[i:i+4] == 'do()':
                do = True
            elif commands[i:i+7] == "don't()":
                do = False
            else:
                pass
    elif commands[i:i+4] != 'mul(':
        pass
    else:
        j = i+4+commands[i+4:].find(')')
        if all((_ in '0123456789,') for _ in commands[i+4:j]) \
                and (len(commands[i+4:j].split(',')) == 2) \
                and do:
            n = list(map(int, commands[i+4:j].split(',')))
            total += n[0] * n[1]

print(f"total one: {total}")



# some testing

def run_commands(commands, switch=False, do=True, verbose=False):
    total = 0 
    mulstr = r"mul[\(][0-9]+,[0-9]+[\)]"
    switchstr = r"do\(\)|don't\(\)"
    if switch:
        regex = mulstr + r'|' + switchstr
    else:
        regex = mulstr
    matches = re.findall(regex, commands)
    if verbose:
        print(matches)
    for command in matches:
        if command == "do()" and switch:
            do = True
        elif command == "don't()" and switch:
            do = False
        elif do:
            try:
                n1, n2 = list(map(int, command.replace('mul(','').replace(')','').split(',')))
                total += n1*n2
            except ValueError:
                print(command)
        else:
            pass
    return total



print(run_commands(input_test1))
print(run_commands(input_3))
print(run_commands(input_test2, switch=True))
print(run_commands(input_3, switch=True))
