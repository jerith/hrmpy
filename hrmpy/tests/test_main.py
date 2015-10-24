import pytest

from hrmpy.main import mainloop
from hrmpy.operations import IllegalOperation
from hrmpy.parser import parse_program, parse_input_data


input = parse_input_data


def program(*lines):
    instructions = ["-- HUMAN RESOURCE MACHINE PROGRAM --"] + list(lines)
    return parse_program("\n".join(instructions))


class TestMainloop(object):
    def test_empty_program(self, cachedsys):
        """
        An empty program produces no output.
        """
        mainloop([], [])
        assert cachedsys.output_data == ""

    def test_empty_program_with_input(self, cachedsys):
        """
        An empty program produces no output even if it gets input.
        """
        mainloop([], input("1 a"))
        assert cachedsys.output_data == ""

    def test_OUTBOX_no_value(self, cachedsys):
        """
        It is an error to OUTBOX a null value.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("OUTBOX"), [])
        assert cachedsys.output_data == ""

    def test_INBOX_OUTBOX_no_input(self, cachedsys):
        """
        A simple copier produces no output if it gets no input.
        """
        mainloop(program("INBOX", "OUTBOX"), [])
        assert cachedsys.output_data == ""

    def test_INBOX_OUTBOX_int(self, cachedsys):
        """
        INBOX will read an integer from the input data and OUTBOX will print
        an integer.
        """
        mainloop(program("INBOX", "OUTBOX"), input("1"))
        assert cachedsys.output_data == "1"

    def test_INBOX_OUTBOX_char(self, cachedsys):
        """
        INBOX will read a character from the input data and OUTBOX will print
        a character.
        """
        mainloop(program("INBOX", "OUTBOX"), input("a"))
        assert cachedsys.output_data == "a"

    def test_INBOX_OUTBOX_JUMP(self, cachedsys):
        """
        A JUMP loop around INBOX OUTBOX will read everything from the input
        data and print it.
        """
        mainloop(
            program("a:", "INBOX", "OUTBOX", "JUMP a"), input("1 a -13"))
        assert cachedsys.output_data == "1 a -13"

    def test_COPYTO_COPYFROM(self, cachedsys):
        """
        COPYTO will store a value in memory and COPYFROM will retrieve it.
        """
        mainloop(
            program(
                "a:", "INBOX", "COPYTO 0", "OUTBOX", "COPYFROM 0", "OUTBOX",
                "JUMP a"),
            input("1 2 a b"))
        assert cachedsys.output_data == "1 1 2 2 a a b b"

    def test_COPYTO_no_value(self, cachedsys):
        """
        It is an error to COPYTO a null value.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("COPYTO 0"), [])
        assert cachedsys.output_data == ""

    def test_COPYFROM_no_value(self, cachedsys):
        """
        It is an error to COPYFROM an empty memory cell.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("COPYFROM 0"), [])
        assert cachedsys.output_data == ""

    def test_COPYTO_COPYFROM_different_addresses(self, cachedsys):
        """
        COPYTO and COPYFROM with different addresses will use different memory
        cells.
        """
        mainloop(
            program(
                "a:", "INBOX", "COPYTO 0", "INBOX", "COPYTO 1", "COPYFROM 0",
                "OUTBOX", "COPYFROM 1", "OUTBOX", "JUMP a"),
            input("1 2 a b"))
        assert cachedsys.output_data == "1 2 a b"

    def test_JUMPZ(self, cachedsys):
        """
        JUMPZ will only jump if the accumulator holds a zero.
        """
        mainloop(
            program("a:", "INBOX", "JUMPZ b", "OUTBOX", "JUMP a", "b:"),
            input("1 2 a b -1 -2 0 1 2"))
        assert cachedsys.output_data == "1 2 a b -1 -2"

    def test_JUMPZ_no_value(self, cachedsys):
        """
        It is an error to JUMPZ with no value.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("a:", "JUMPZ a"), [])
        assert cachedsys.output_data == ""

    def test_JUMPN(self, cachedsys):
        """
        JUMPN will only jump if the accumulator holds a negative integer.
        """
        mainloop(
            program("a:", "INBOX", "JUMPN b", "OUTBOX", "JUMP a", "b:"),
            input("1 2 a b 0 -1 0 1 2 -2"))
        assert cachedsys.output_data == "1 2 a b 0"

    def test_JUMPN_no_value(self, cachedsys):
        """
        It is an error to JUMPN with no value.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("a:", "JUMPN a"), [])
        assert cachedsys.output_data == ""

    def test_ADD_ints(self, cachedsys):
        """
        ADD will add two numbers.
        """
        mainloop(
            program("INBOX", "COPYTO 0", "INBOX", "ADD 0", "OUTBOX"),
            input("2 3"))
        assert cachedsys.output_data == "5"

    def test_ADD_no_value(self, cachedsys):
        """
        It is an error to ADD with one or more values missing.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("ADD 0"), [])
        assert cachedsys.output_data == ""

        with pytest.raises(IllegalOperation):
            mainloop(program("INBOX", "ADD 0"), input("1"))
        assert cachedsys.output_data == ""

        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "OUTBOX", "ADD 0"), input("1"))
        assert cachedsys.output_data == "1"

    def test_SUB_ints(self, cachedsys):
        """
        SUB will subtract two numbers.
        """
        mainloop(
            program("INBOX", "COPYTO 0", "INBOX", "SUB 0", "OUTBOX"),
            input("3 2"))
        assert cachedsys.output_data == "-1"

    def test_SUB_no_value(self, cachedsys):
        """
        It is an error to SUB with one or more values missing.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("SUB 0"), [])
        assert cachedsys.output_data == ""

        with pytest.raises(IllegalOperation):
            mainloop(program("INBOX", "SUB 0"), input("1"))
        assert cachedsys.output_data == ""

        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "OUTBOX", "SUB 0"), input("1"))
        assert cachedsys.output_data == "1"

    def test_ADD_chars(self, cachedsys):
        """
        ADD will not add two characters.
        """
        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "INBOX", "ADD 0", "OUTBOX"),
                input("a b"))
        assert cachedsys.output_data == ""

    def test_SUB_chars(self, cachedsys):
        """
        SUB will subtract two characters.
        """
        mainloop(
            program("INBOX", "COPYTO 0", "INBOX", "SUB 0", "OUTBOX"),
            input("b a"))
        assert cachedsys.output_data == "-1"

    def test_ADD_int_char(self, cachedsys):
        """
        ADD will not add an integer and a character.
        """
        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "INBOX", "ADD 0", "OUTBOX"),
                input("a 2"))
        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "INBOX", "ADD 0", "OUTBOX"),
                input("1 b"))
        assert cachedsys.output_data == ""

    def test_SUB_int_char(self, cachedsys):
        """
        SUB will not subtract an integer and a character.
        """
        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "INBOX", "SUB 0", "OUTBOX"),
                input("a 2"))
        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "INBOX", "SUB 0", "OUTBOX"),
                input("1 b"))
        assert cachedsys.output_data == ""

    def test_BUMPUP_int(self, cachedsys):
        """
        BUMPUP increments and retrieves a value.
        """
        mainloop(
            program("a:", "INBOX", "COPYTO 0", "BUMPUP 0", "OUTBOX", "JUMP a"),
            input("1 0 -1 -2"))
        assert cachedsys.output_data == "2 1 0 -1"

    def test_BUMPUP_char(self, cachedsys):
        """
        A character cannot be incremented.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("INBOX", "COPYTO 0", "BUMPUP 0"), input("a"))
        assert cachedsys.output_data == ""

    def test_BUMPUP_no_value(self, cachedsys):
        """
        It is an error to increment a missing value.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("BUMPUP 0"), [])
        assert cachedsys.output_data == ""

    def test_BUMPDN_int(self, cachedsys):
        """
        BUMPDN decrements and retrieves a value.
        """
        mainloop(
            program("a:", "INBOX", "COPYTO 0", "BUMPDN 0", "OUTBOX", "JUMP a"),
            input("2 1 0 -1"))
        assert cachedsys.output_data == "1 0 -1 -2"

    def test_BUMPDN_char(self, cachedsys):
        """
        A character cannot be decremented.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("INBOX", "COPYTO 0", "BUMPDN 0"), input("a"))
        assert cachedsys.output_data == ""

    def test_BUMPDN_no_value(self, cachedsys):
        """
        It is an error to decrement a missing value.
        """
        with pytest.raises(IllegalOperation):
            mainloop(program("BUMPDN 0"), [])
        assert cachedsys.output_data == ""
