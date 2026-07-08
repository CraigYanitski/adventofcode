from colorama import init, Fore, Style
import re
import os
from pprint import pprint
from copy import deepcopy

init(autoreset=True)

input_test: str = \
"""Register A: 729
   Register B: 0
   Register C: 0
   
   Program: 0,1,5,4,3,0
""".replace('   ', '')

input_test_2: str = \
"""Register A: 2024
   Register B: 0
   Register C: 0
   
   Program: 0,1,5,4,3,0
""".replace('   ', '')

input_test_3: str = \
"""Register A: 10
   Register B: 0
   Register C: 0
   
   Program: 5,0,5,1,5,4
""".replace('   ', '')

input_test_4: str = \
"""Register A: 2024
   Register B: 0
   Register C: 0
   
   Program: 0,3,5,4,3,0
""".replace('   ', '')

input_17: str = open("input_17").read()


registers: dict = {"Register A": 0,
                   "Register B": 0,
                   "Register C": 0}
inst_px: int = 0

def combo_ops(op) -> int:
    match op:
        case 0:
            return 0
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 3
        case 4:
            return registers["Register A"]
        case 5:
            return registers["Register B"]
        case 6:
            return registers["Register C"]
        case _:
            raise ValueError(f"combo opcode {op} used: program not valid")

def adv(op) -> None:
    #print("adv")
    global inst_px
    global registers
    registers["Register A"] = registers["Register A"] // (2**combo_ops(op))
    inst_px += 2
    return

def bxl(op) -> None:
    #print("bxl")
    global inst_px
    global registers
    registers["Register B"] = registers["Register B"] ^ op
    inst_px += 2
    return

def bst(op) -> None:
    #print("bst")
    global inst_px
    global registers
    registers["Register B"] = combo_ops(op) % 8
    inst_px += 2
    return

def jnz(op) -> None:
    #print("jnz")
    global inst_px
    global registers
    if registers["Register A"]:
        inst_px = op
    else:
        inst_px += 2
    return

def bxc(op) -> None:
    #print("bxc")
    global inst_px
    global registers
    registers["Register B"] = registers["Register B"] ^ registers["Register C"]
    inst_px += 2
    return

def out(op) -> int:
    #print("out")
    global inst_px
    inst_px += 2
    return combo_ops(op) % 8

def bdv(op) -> None:
    #print("bdv")
    global inst_px
    global registers
    registers["Register B"] = registers["Register A"] // (2**combo_ops(op))
    inst_px += 2
    return

def cdv(op) -> None:
    #print("cdv")
    global inst_px
    global registers
    registers["Register C"] = registers["Register A"] // (2**combo_ops(op))
    inst_px += 2
    return

def r_adv(op) -> None:
    #print("adv")
    global inst_px
    global registers
    registers["Register A"] = registers["Register A"] // (2**combo_ops(op))
    inst_px += 2
    return

def r_bxl(op) -> None:
    #print("bxl")
    global inst_px
    global registers
    registers["Register B"] = registers["Register B"] ^ op
    inst_px += 2
    return

def r_bst(op) -> None:
    #print("bst")
    global inst_px
    global registers
    registers["Register B"] = combo_ops(op) % 8
    inst_px += 2
    return

def r_jnz(op) -> None:
    #print("jnz")
    global inst_px
    global registers
    if registers["Register A"]:
        inst_px = op
    else:
        inst_px += 2
    return

def r_bdv(op) -> None:
    #print("bdv")
    global inst_px
    global registers
    registers["Register B"] = registers["Register A"] // (2**combo_ops(op))
    inst_px += 2
    return

def r_cdv(op) -> None:
    #print("cdv")
    global inst_px
    global registers
    registers["Register C"] = registers["Register A"] // (2**combo_ops(op))
    inst_px += 2
    return

opcodes: dict = {0: adv,
                 1: bxl,
                 2: bst,
                 3: jnz,
                 4: bxc,
                 5: out,
                 6: bdv,
                 7: cdv,}


def compute(text, part=1, debug=False, test=False, verbose=False) -> (int|str):
    global inst_px
    print(text)
    reg_init, commands = text.split('\n\n')
    inst_px = 0
    reset_registers()
    for line in reg_init.split('\n'):
        reg, v = line.split(': ')
        registers[reg] = int(v)
    # if  part == 2:
    #     registers["Register A"] = 117440
    commands: str = commands.strip('\n').split(': ')[1].replace(',', '')
    out: list = assembler(commands, debug=debug)
    if part == 2:
        a = disassembler(commands)
        return a
    else:
        print(commands)
        pprint(registers)
        print()
        pprint(registers)
        print()
        print(f"Output: {','.join(out)}\n")
    return ','.join(out)

def reset_registers() -> None:
    registers["Register A"] = 0
    registers["Register B"] = 0
    registers["Register C"] = 0
    return

def assembler(commands, debug=False) -> list:
    global inst_px
    out: list = []
    counter: int = 0
    while inst_px < len(commands) and counter < len(commands)**3:
        opcode: int = int(commands[inst_px])
        op: int = int(commands[inst_px+1])
        o = opcodes[opcode](op)
        #print(inst_px)
        if not o is None:
            out.append(str(o))
        if debug:
            _: int = os.system('clear')
            print()
            print(f"Register A: {registers['Register A']}")
            print(f"Register B: {registers['Register B']}")
            print(f"Register C: {registers['Register C']}")
            for i in range(len(commands)):
                if i == (inst_px-2) % len(commands):
                    print(Fore.YELLOW + Style.BRIGHT + commands[i], end='')
                else:
                    print(commands[i], end='')
            print()
            print()
            print(f"Output: {','.join(out)}")
            input()
        counter += 1
        #if counter > len(commands)**3:
        #    break
        #print(counter)
    return out

def disassembler(commands) -> int:
    global inst_px
    a: int = 2024
    inc: int = 0
    out: list = []
    while ''.join(out) != commands and a < 10**15:
        reset_registers()
        inc += 1
        print(a + inc)
        inst_px = 0
        registers["Register A"] = a + inc
        if (inc % 8) == 0:
            inc: int = 0
            a: int = a << 3
        out = assembler(commands, debug=False)
        if ''.join(out) == commands:
            print(Fore.GREEN + f"Match found!!  A={a}")
            break
    return a

def run_program(a) -> list:
    out: list = []
    while a:
        b = a % 8 ^3
        out.append(str(b ^ 5 ^ (a >> b) % 8))
        a //= 8
        #print(out)
    return out


def run_test(text, test_inputs=[('', 0)], part=1, debug=False) -> None:
    res: int|str = compute(test_inputs[0][0], test=True, part=part, debug=debug, verbose=True)
    print()
    if res == test_inputs[0][1]:
        print(Fore.GREEN + "Part " + 'I'*part + " test passed!!")
        if len(test_inputs) > 1:
            res: int|str = compute(test_inputs[1][0], test=True, debug=debug)
            if res == test_inputs[1][1]:
                if len(test_inputs) > 2:
                    res: int|str = compute(test_inputs[2][0], test=True, debug=debug)
                    if res == test_inputs[2][1]:
                        print(Fore.GREEN + "All tests passed!!")
        res: int|str = compute(text, part=part, verbose=False, debug=debug)
    else:
        print(Fore.RED + "Part " + 'I'*part + " test failed...")
    print()
    print("Part " + 'I'*part + f": {res}")


if __name__ == "__main__":
    run_test(input_17, [(input_test_3, "0,1,2"), (input_test_2, "4,2,5,6,7,7,7,7,3,1,0"), (input_test, "4,6,3,5,6,3,5,2,1,0")], part=1)
    print('='*10)
    # run_test(input_17, [(input_test_4, 117440)], part=2)
    print(','.join(run_program(55593699)))
    code: str = "2413750315445530"
    p: list = [0]
    for i in range(len(code)):
        p: list = [
            n * 8 + a 
            for n in p 
            for a in range(8) 
            if code[-i-1:] == ''.join(run_program(n * 8 + a))
        ]
        print(p)
    print(f"minimum A: {p[0]}")
    for a in ('2', '22', '223', '2234', '1', '12', '123', '1234', '76543210', '10', '1234567',
              '10', '1', '2', '3', '4', '5', '6', '7'):
        print(f"A: {a} -> ", ','.join(run_program(int(a, 8))))
    a = ''
    for i in range(len(code)):
        res = list(map(lambda x: run_program(int(a+str(x), 8)), range(8)))
        for j, r in enumerate(res):
            if ''.join(r) == code[-i-1:]:
                a += str(j)
                print(i, a)
    print(int(a))
    
