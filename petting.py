import string

STACK_LENGTH = 10

def cmpl(petting_code):
    """ Transforms Brainfuck-with-variables to
    normal Brainfuck code."""
    variables = {
        'M': 0 # beginning of memory
    }

    # move right of the stack pointer and
    # enter the value space
    brainfuck = '>' * 5

    for ch in petting_code:
        if ch not in string.ascii_lowercase + 'M': # the stack pointer
            if ch == '<':
                brainfuck += '<<' # every move translates to two moves
            elif ch == '>':
                brainfuck += '>>'
            elif ch == '{':
                brainfuck += '<'
            elif ch == '}':
                brainfuck += '>'
            else:
                brainfuck += ch
            continue

        var = ch
        if var not in variables:
            variables[var] = STACK_LENGTH + len(variables) + 1

        # 1. move one left to enter adress space
        # 2. move left until you reach the stack pointer
        # 3. move left until you reach the start of the memory
        # 3. go right n cells
        find_var_code = '<[<<]<<[<<]' + ('>>' * variables[var]) + '>'

        brainfuck += find_var_code

    return optimize(brainfuck)

def optimize(brainfuck_code):
    replaced_something = True
    while True:
        if brainfuck_code.find('><') != -1:
            brainfuck_code = brainfuck_code.replace('><', '')
        elif brainfuck_code.find('<>') != -1:
            brainfuck_code = brainfuck_code.replace('<>', '')
        elif brainfuck_code.find('-+') != -1:
            brainfuck_code = brainfuck_code.replace('-+', '')
        elif brainfuck_code.find('+-') != -1:
            brainfuck_code = brainfuck_code.replace('+-', '')
        else:
            replaced_something = False
        if not replaced_something:
            return brainfuck_code
