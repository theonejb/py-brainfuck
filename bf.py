"""
implements a basic brain fuck interpreter.
"""

import sys

# import custom getch() like function
from getch import _Getch

class BFVM(object):
    """
    the brainf***VirtualMachine class. implements all functionality required for
    running a brainf*** program.
    """
    # consts to define brainf*** to operand handler mapping
    ops = {
            '>': 'increment_dp', # increment data pointer
            '<': 'decrement_dp', # decrement data pointer
            '+': 'increment_b',  # increment current byte
            '-': 'decrement_b',  # decrement current byte
            '.': 'output_b',     # output current byte
            ',': 'input_b',      # read/save at current byte
            '[': 'jmpfifz',      # jmp forward to matching ] if current data byte zero
            ']': 'jmpbifnz',      # jmp back to matching ] if current data byte non-zero
            }
    dataSize = 30000

    def __init__(self, filename=None, program=None):
        """
        requires either inputFileName or programData (which is a string with the
        brainf*** program.
        """
        if filename is None and program is None:
            raise ValueError("inputFileName and programData can not both be None")
        if filename:
            f = open(filename, 'r')
            self._prog = f.read()
            f.close()
        else:
            self._prog = program

    def run(self):
        # construct the data stream and init relevant vars
        self._data = bytearray(self.dataSize)
        self._dp = 0
        self._ip = 0
        while True:
            try:
                char = self._prog[self._ip]
                self._ip = self._ip + 1
            except IndexError:
                break
            try:
                # get the opcode handler
                oph = self.ops[char]
            except KeyError:
                continue
            getattr(self, oph)()
        print
    
    def increment_dp(self):
        self._dp = self._dp + 1
        if self._dp > self.dataSize:
            self._dp = 0
    
    def decrement_dp(self):
        self._dp = self._dp - 1
        if self._dp < 0:
            self._dp = 0

    def increment_b(self):
        try:
            self._data[self._dp] = self._data[self._dp] + 1
        except ValueError:
            self._data[self._dp] = 0

    def decrement_b(self):
        try:
            self._data[self._dp] = self._data[self._dp] - 1
        except ValueError:
            self._data[self._dp] = 255

    def output_b(self):
        sys.stdout.write(chr(self._data[self._dp]))

    def input_b(self):
        self._data[self._dp] = _Getch()()

    def jmpfifz(self):
        if self._data[self._dp] != 0:
            return

        stack = 1
        while stack != 0:
            if self._prog[self._ip] == '[':
                stack = stack + 1
            elif self._prog[self._ip] == ']':
                stack = stack - 1
            self._ip = self._ip + 1

    def jmpbifnz(self):
        if self._data[self._dp] == 0:
            return
        # since the instruction pointer is moved +1 before we're called, move
        # it -2, since we're searching backwards
        self._ip = self._ip - 2

        stack = 1
        while stack != 0:
            if self._prog[self._ip] == ']':
                stack = stack + 1
            elif self._prog[self._ip] == '[':
                stack = stack - 1
            self._ip = self._ip - 1
        self._ip  = self._ip + 1

