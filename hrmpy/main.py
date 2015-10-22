import os
import sys

import hrmpy.operations as ops
from hrmpy.parser import parse_program, parse_input_data


class Memory(object):
    def __init__(self):
        self._cells = {}

    def get(self, addr):
        return self._cells[addr]

    def set(self, addr, value):
        self._cells[addr] = value


class Program(object):
    def __init__(self, operations):
        self._jump_labels = {}
        self._comments = {}
        self._comment_values = {}
        self._label_values = {}
        self._operations = []
        self._build_program(operations)

    def __str__(self):
        # TODO: Pretty-print.
        bits = ['<Program']
        bits.extend(str(op) for op in self._operations)
        bits.extend([str(self._jump_labels), '>'])
        return '\n  '.join(bits)

    def _build_program(self, operations):
        for op in operations:
            if isinstance(op, ops.JumpLabel):
                assert op.label not in self._jump_labels
                self._jump_labels[op.label] = len(self._operations)
            elif isinstance(op, ops.Comment):
                # Ignore for now.
                pass
            elif isinstance(op, ops.Definition):
                # Ignore for now.
                pass
            else:
                assert not isinstance(op, ops.PseudoOperation)
                self._operations.append(op)

    def __getitem__(self, index):
        return self._operations[index]

    def __len__(self):
        return len(self._operations)


class Accumulator(object):
    def __init__(self):
        self.empty = True
        self.value = None

    def set(self, value):
        self.empty = False
        self.value = value

    def get(self):
        assert not self.empty, "Accumulator is empty."
        return self.value

    def clear(self):
        self.empty = True


def mainloop(program, input_data):
    memory = Memory()
    acc = Accumulator()
    pc = 0
    while 0 <= pc < len(program):
        op = program[pc]
        if op.name == 'INBOX':
            if not input_data:
                print "-- DONE --"
                return
            acc.set(input_data.pop(0))
        elif op.name == 'OUTBOX':
            print acc.get().tostr()
            acc.clear()
        elif op.name == 'JUMP':
            pc = program._jump_labels[op.label] - 1
        elif op.name == 'JUMPZ':
            if acc.get().zero():
                pc = program._jump_labels[op.label] - 1
        elif op.name == 'JUMPN':
            if acc.get().negative():
                pc = program._jump_labels[op.label] - 1
        elif op.name == 'COPYTO':
            memory.set(op.addr, acc.get())
        elif op.name == 'COPYFROM':
            acc.set(memory.get(op.addr))
        elif op.name == 'ADD':
            acc.set(acc.get().add(memory.get(op.addr)))
        elif op.name == 'SUB':
            acc.set(acc.get().sub(memory.get(op.addr)))
        else:
            assert False, "Unknown op: %s" % (op,)
        pc += 1


def read(filename):
    fp = os.open(filename, os.O_RDONLY, 0777)
    program_contents = ""
    while True:
        data = os.read(fp, 4096)
        if len(data) == 0:
            break
        program_contents += data
    os.close(fp)
    return program_contents


def entry_point(argv):
    try:
        program_filename = argv[1]
    except IndexError:
        print "I can't run a program if you don't give me one."
        return 1
    try:
        input_filename = argv[2]
    except IndexError:
        print "I can't run a program if you don't give me input."
        return 1
    try:
        memory_filename = argv[3]
    except IndexError:
        memory_filename = None
    program = Program(parse_program(read(program_filename)))
    input_data = parse_input_data(read(input_filename))
    assert memory_filename is None, "Not implemented yet."
    mainloop(program, input_data)
    return 0


def target(driver, args):
    driver.exe_name = 'hrmpy-%(backend)s'
    return entry_point, None


if __name__ == '__main__':
    entry_point(sys.argv)
