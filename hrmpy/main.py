import os

from hrmpy import operations as ops
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


def not_none(value, msg):
    ops.check_legal(value is not None, "Nothing to " + msg)
    return value


def mainloop(program, input_data):
    program = Program(program)
    memory = Memory()
    acc = None
    pc = 0
    while 0 <= pc < len(program):
        op = program[pc]
        if op.name == 'INBOX':
            if not input_data:
                return
            acc = input_data.pop(0)
        elif op.name == 'OUTBOX':
            print not_none(acc, "OUTBOX").tostr()
            acc = None
        elif op.name == 'JUMP':
            pc = program._jump_labels[op.label] - 1
        elif op.name == 'JUMPZ':
            if not_none(acc, "compare").zero():
                pc = program._jump_labels[op.label] - 1
        elif op.name == 'JUMPN':
            if not_none(acc, "compare").negative():
                pc = program._jump_labels[op.label] - 1
        elif op.name == 'COPYTO':
            memory.set(op.addr, not_none(acc, "COPYTO"))
        elif op.name == 'COPYFROM':
            acc = memory.get(op.addr)
        elif op.name == 'ADD':
            acc = not_none(acc, "ADD to").add(memory.get(op.addr))
        elif op.name == 'SUB':
            acc = not_none(acc, "SUB from").sub(memory.get(op.addr))
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
    program = parse_program(read(program_filename))
    input_data = parse_input_data(read(input_filename))
    assert memory_filename is None, "Not implemented yet."
    mainloop(program, input_data)
    return 0
