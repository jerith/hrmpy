"""
Operations defined for this interpreter.
"""


NULLARY_OPERATIONS = [
    'INBOX',
    'OUTBOX',
]

MEMORY_OPERATIONS = [
    'COPYTO',
    'COPYFROM',
    'ADD',
    'SUB',
]

JUMP_OPERATIONS = [
    'JUMP',
    'JUMPZ',
    'JUMPN',
]


class Operation(object):
    """
    An operation the program can execute.
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class NullaryOperation(Operation):
    """
    An operation that has no parameters.
    """
    pass


class MemoryOperation(Operation):
    """
    An operation that operates on a memory address.
    """
    def __init__(self, name, addr):
        Operation.__init__(self, name)
        self.addr = addr

    def __str__(self):
        return "% -8s %s" % (self.name, self.addr)


class JumpOperation(Operation):
    """
    An operation that modifies the program counter.
    """
    def __init__(self, name, label):
        Operation.__init__(self, name)
        self.label = label

    def __str__(self):
        return "% -8s %s" % (self.name, self.label)


class PseudoOperation(Operation):
    """
    Not actually an operation. A placeholder for parsing.
    """


class JumpLabel(PseudoOperation):
    def __init__(self, label):
        Operation.__init__(self, 'jumplabel')
        self.label = label


class Comment(PseudoOperation):
    def __init__(self, comment_number):
        Operation.__init__(self, 'comment')
        self.comment_number = comment_number


class Definition(PseudoOperation):
    def __init__(self, instructions):
        Operation.__init__(self, 'definition')
        self.instructions = instructions


class Value(object):
    """
    A value.
    """


class Integer(Value):
    """
    An integer.
    """
    def __init__(self, integer):
        self.integer = integer


class Character(Value):
    """
    A character.
    """
    def __init__(self, character):
        self.character = character
