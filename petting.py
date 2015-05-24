import string

def transform(petting_code):
    """ Transforms Brainfuck-with-variables to
    normal Brainfuck code."""
    variables = {}
    
    # move left so leftmost location is empty.
    # the value 1 in the address space represents
    # the beginning of it.
    brainfuck = '>>>'
    
    for ch in petting_code:
        if ch not in string.ascii_lowercase:
            if ch == '<':
                brainfuck += '<<' # every move translates to two moves
            elif ch == '>':
                brainfuck += '>>'
            else:
                brainfuck += ch
            continue
        var = ch
        if var not in variables:
            variables[var] = len(variables) + 1

        # 1. move one left to enter adress space
        # 2. move left until you encounter a zero (starting address)
        # 3. go right n cells
        find_var_code = '<[<<]' + ('>>' * variables[var]) + '>'

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
