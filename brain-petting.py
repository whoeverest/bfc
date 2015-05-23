import string

def transform(petting_code):
    """ Transforms Brainfuck-with-variables to
    normal Brainfuck code."""
    variables = {}
    brainfuck = '>' # move left so leftmost location is empty
    
    for ch in petting_code:
        print ch
        if ch not in string.ascii_lowercase:
            brainfuck += ch
            continue
        var = ch
        if var not in variables:
            variables[var] = len(variables) + 1
        find_var_code = '[<]' + ('>') * variables[var]
        brainfuck += find_var_code

    return brainfuck


compiled = transform('a+b++c+++')

print compiled