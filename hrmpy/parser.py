import hrmpy.operations as ops


def _parse_instructions(instructions):
    operations = []
    _parse_header(instructions)
    while instructions:
        op = _parse_instruction(instructions)
        if op is not None:
            operations.append(op)
    return operations


def _parse_header(instructions):
    while instructions:
        instruction = instructions.pop(0).strip()
        if instruction == '-- HUMAN RESOURCE MACHINE PROGRAM --':
            return
    raise RuntimeError("No program found.")


def _parse_instruction(instructions):
    instruction = instructions.pop(0).strip()
    if not instruction:
        return
    # Non-operation things.
    if instruction.endswith(':'):
        return ops.JumpLabel(instruction[:-1])
    if instruction.startswith('DEFINE '):
        return _parse_define(instruction, instructions)
    if instruction.startswith('COMMENT '):
        return ops.Comment(instruction)
    # Operation things.
    op, data = _splitop(instruction)
    if op in ops.NULLARY_OPERATIONS:
        return ops.NullaryOperation(instruction)
    if op in ops.MEMORY_OPERATIONS:
        return ops.MemoryOperation(op, int(data))
    elif op in ops.JUMP_OPERATIONS:
        return ops.JumpOperation(op, data)
    assert False, "Not implemented: %s" % (instruction,)


def _splitop(instruction):
    op = ""
    for i, char in enumerate(instruction):
        if char in " \t\r\n":
            return op, instruction[i:].strip()
        op += char
    return instruction, ""


def _parse_define(instruction, instructions):
    define_bits = []
    # Ignore for now.
    while instruction:
        define_bits.append(instruction)
        instruction = instructions.pop(0).strip()
    return ops.Definition(define_bits)


def parse_program(text):
    return _parse_instructions(text.splitlines())


def parse_input_data(text):
    input_data = []
    datum = ""
    for char in text:
        if char in " \t\r\n":
            if datum:
                input_data.append(_parse_input_datum(datum))
                datum = ""
        else:
            datum += char
    if datum:
        input_data.append(_parse_input_datum(datum))
    return input_data


characters = ''.join(chr(c) for c in range(ord('a'), ord('z') + 1))


def _parse_input_datum(datum):
    if len(datum) == 1 and datum in characters:
        return ops.Character(datum)
    return ops.Integer(int(datum))
