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
    'BUMPUP',
    'BUMPDN',
]

JUMP_OPERATIONS = [
    'JUMP',
    'JUMPZ',
    'JUMPN',
]


def check_legal(is_legal, msg):
    if not is_legal:
        raise IllegalOperation(msg)


class IllegalOperation(Exception):
    pass


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


class Memset(PseudoOperation):
    def __init__(self, addr, value):
        Operation.__init__(self, '.memset')
        self.addr = addr
        self.value = value

    def __str__(self):
        return "%s %s %s" % (self.name, self.addr, self.value.tostr())


class Value(object):
    """
    A value.
    """

    def __eq__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def add(self, other):
        raise IllegalOperation("Can't add these.")

    def sub(self, other):
        raise IllegalOperation("Can't sub these.")

    def tostr(self):
        assert False, "Not implemented"

    def zero(self):
        return False

    def negative(self):
        return False


class Integer(Value):
    """
    An integer.
    """
    def __init__(self, integer):
        self.integer = integer

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.integer == other.integer

    def add(self, other):
        check_legal(isinstance(other, Integer), "Can't add these.")
        return Integer(self.integer + other.integer)

    def sub(self, other):
        check_legal(isinstance(other, Integer), "Can't sub these.")
        return Integer(self.integer - other.integer)

    def tostr(self):
        return str(self.integer)

    def zero(self):
        return self.integer == 0

    def negative(self):
        return self.integer < 0


class Character(Value):
    """
    A character.
    """
    def __init__(self, character):
        # RPython requires proof that this is a character and not a string.
        assert len(character) == 1
        self.character = character[0]

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.character == other.character

    def tostr(self):
        return self.character

    def sub(self, other):
        check_legal(isinstance(other, Character), "Can't sub these.")
        return Integer(ord(self.character) - ord(other.character))
