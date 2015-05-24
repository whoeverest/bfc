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
from petting import transform

class EndOfProgram(Exception):
    pass

class Brainfuck(object):
    def __init__(self, code, mapped_memory=True, size=30000):
        self.source_index = 0
        self.code = ''.join([ch for ch in code if ch in '<>-+[],.'])
        self.pointer = 0
        
        if mapped_memory:
            self.memory = [0] + ([0, 1] * (size / 2))
        else:
            self.code = [0] * size

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

        if self.memory[self.pointer] < 0:
            raise ValueError('Memory cannot be negative')

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
            self.source_index = self.code[self.source_index:].find(']')

    def end_loop(self):
        if self.memory[self.pointer] == 0:
            self.source_index += 1
        else:
            self.source_index = self.code[:self.source_index + 1].rfind('[')

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

    def __str__(self):
        memory = ', '.join(map(str, self.memory[:10]))
        pointer = ' ' * (self.pointer * 3) + '^'
        return '\n'.join([memory, pointer])

b = Brainfuck(transform("a+b++c+++"))

while True:
    try:
        print b
        b.step()
        sleep(.5)
    except EndOfProgram:
        exit(0)