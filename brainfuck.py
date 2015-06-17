#!/usr/bin/env python

# brainfuck

# >     Increment the pointer.
# <     Decrement the pointer.
# +     Increment the byte at the pointer.
# -     Decrement the byte at the pointer.
# .     Output the byte at the pointer.
# ,     Input a byte and store it in the byte at the pointer.
# [     Jump forward past the matching ] if the byte at the pointer is zero.
# ]     Jump backward to the matching [ unless the byte at the pointer is zero.

from time import sleep
from termcolor import colored
from petting import cmpl

def map_memory(code, memory, free_memory=4, stack_size=4):
    # The start of the memory is reserved for registers
    instruction_reg = [0, 0]
    memory_reg = [0, 0]
    temp_reg = [0, 0]

    # Code segment, each instruction is 4 cells wide
    # [addr, lbracket, rbracket, value]
    code_segment = [0, 0, 0, 0, 0]

    for instr in code:
        code_segment.extend([1, 1, 0, 0, instr])

    # Stack
    stack_segment = [0, 0] + ([1, 0] * (stack_size - 1))

    # RAM
    ram_segment = []
    ram_segment.extend([0, 0])

    for mem in memory:
        ram_segment.extend([1, mem])

    ram_segment.extend([1, 0] * free_memory)
    ram_segment.extend([0, 0]) # end of memory

    return instruction_reg + memory_reg + temp_reg + \
           code_segment + \
           stack_segment + \
           ram_segment

def print_mapped_memory(memory):
    print 'IR', memory[0:2]
    print 'MR', memory[2:4]
    print 'TR', memory[4:6]

    print 'code:'
    print ' A  C  L  R  V'
    print memory[6:11]
    
    i = 11

    while memory[i] == 1:
        print memory[i:i+5]
        i += 5

    print 'stack:'
    print memory[i:i+2]

    i += 2

    while memory[i] == 1:
        print memory[i:i+2]
        i += 2

    print 'memory:'
    print memory[i:i+2]

    i += 2

    while memory[i] == 1:
        print memory[i:i+2]
        i += 2


mapped = map_memory('+++---', [5, 0, 1, 1, 20, 30])
print_mapped_memory(mapped)

exit(0)

class EndOfProgram(Exception):
    pass

class Brainfuck(object):
    def __init__(self, code, memory, size=30000):
        self.source_index = 0
        self.code = ''.join([ch for ch in code if ch in '<>-+[],.'])
        self.pointer = 0
        self.brackets = {}

        self.map_brackets()

        if not memory:
            self.memory = [0] * size

    def map_brackets(self):
        i = 0
        stack = []
        for pos, ch in enumerate(self.code):
            if ch == '[':
                stack.append(pos)
            elif ch == ']':
                starting_position = stack.pop()
                self.brackets[starting_position] = pos
                self.brackets[pos] = starting_position

    def inc_pointer(self):
        self.pointer += 1
        self.source_index += 1

    def dec_pointer(self):
        self.pointer -= 1
        self.source_index += 1

    def inc_value(self):
        self.memory[self.pointer] += 1
        self.source_index += 1

    def dec_value(self):
        self.memory[self.pointer] -= 1
        self.source_index += 1

        # if self.memory[self.pointer] < 0:
        #     raise ValueError('Memory cannot be negative')

    def print_ch(self):
        print self.memory[self.pointer]
        self.source_index += 1

    def get_ch(self):
        self.memory[self.pointer] = raw_input()[0]
        self.source_index += 1

    def start_loop(self):
        if self.memory[self.pointer]:
            self.source_index += 1
        else:
            self.source_index = self.brackets[self.source_index]

    def end_loop(self):
        if self.memory[self.pointer] == 0:
            self.source_index += 1
        else:
            self.source_index = self.brackets[self.source_index]

    def execute(self, cmd):
        commands = {
            '>': self.inc_pointer,
            '<': self.dec_pointer,
            '+': self.inc_value,
            '-': self.dec_value,
            '.': self.print_ch,
            ',': self.get_ch,
            '[': self.start_loop,
            ']': self.end_loop,
        }

        commands[cmd]()

    def step(self):
        try:
            cmd = self.code[self.source_index]
            self.execute(cmd)
        except IndexError:
            raise EndOfProgram

        if self.pointer < 0:
            raise ValueError("Pointer can't be negative")

    def run(self, print_state=False, sleep_time=0.0):
        while True:
            try:
                if print_state:
                    print self
                self.step()
                if sleep_time:
                    sleep(sleep_time)
            except EndOfProgram:
                exit(0)

    def __str__(self):
        printable_string = '['
        mem_slice = self.memory[:40]
        length = len(mem_slice)

        for i, m in enumerate(mem_slice):
            if i == self.pointer:
                printable_string += colored(str(m), 'red')
            else:
                printable_string += str(m)

            if i != length - 1:
                printable_string += ', '

        printable_string += ']'
        
        return printable_string + '\r'
