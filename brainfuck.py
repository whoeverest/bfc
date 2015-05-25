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

class EndOfProgram(Exception):
    pass

class Brainfuck(object):
    def __init__(self, code, mapped_memory=True, size=30000):
        self.source_index = 0
        self.code = ''.join([ch for ch in code if ch in '<>-+[],.'])
        self.pointer = 0
        self.brackets = {}

        self.map_brackets()
        
        if mapped_memory:
            # The first two cells mark the start of the memory
            # The next two cells mark the stack pointer
            # The rest of the memory is marked with 1's
            self.memory = [0, 0, 0, 0] + ([1, 0] * (size / 2))
        else:
            self.code = [0] * size

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
