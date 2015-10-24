import pytest

from hrmpy.main import mainloop
from hrmpy.operations import IllegalOperation
from hrmpy.parser import parse_program, parse_input_data


def program(*lines):
    instructions = ["-- HUMAN RESOURCE MACHINE PROGRAM --"] + list(lines)
    return parse_program("\n".join(instructions))


class TestMainloop(object):
    def test_empty_program(self, capsys):
        """
        An empty program produces no output.
        """
        mainloop([], [])
        out = capsys.readouterr()[0]
        assert out == ""

    def test_empty_program_with_input(self, capsys):
        """
        An empty program produces no output even if it gets input.
        """
        mainloop([], parse_input_data("1 a"))
        out = capsys.readouterr()[0]
        assert out == ""

    def test_INBOX_OUTBOX_no_input(self, capsys):
        """
        A simple copier produces no output if it gets no input.
        """
        mainloop(program("INBOX", "OUTBOX"), [])
        out = capsys.readouterr()[0]
        assert out == ""

    def test_INBOX_OUTBOX(self, capsys):
        """
        A simple copier produces output if it gets input.
        """
        mainloop(program("INBOX", "OUTBOX"), parse_input_data("1"))
        out = capsys.readouterr()[0]
        assert out == "1\n"

    def test_copy_loop(self, capsys):
        """
        A copy loop produces output if it gets input.
        """
        mainloop(
            program("a:", "INBOX", "OUTBOX", "JUMP a"),
            parse_input_data("1 a -13"))
        out = capsys.readouterr()[0]
        assert out == "1\na\n-13\n"

    def test_adder(self, capsys):
        """
        An adder will add two numbers.
        """
        mainloop(
            program("INBOX", "COPYTO 0", "INBOX", "ADD 0", "OUTBOX"),
            parse_input_data("2 3"))
        out = capsys.readouterr()[0]
        assert out == "5\n"

    def test_subber(self, capsys):
        """
        A subber will sub two numbers.
        """
        mainloop(
            program("INBOX", "COPYTO 0", "INBOX", "SUB 0", "OUTBOX"),
            parse_input_data("3 2"))
        out = capsys.readouterr()[0]
        assert out == "-1\n"

    def test_adder_char(self, capsys):
        """
        An adder will not add two characters.
        """
        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "INBOX", "ADD 0", "OUTBOX"),
                parse_input_data("a b"))
        out = capsys.readouterr()[0]
        assert out == ""

    def test_subber_char(self, capsys):
        """
        A subber will sub two characters.
        """
        mainloop(
            program("INBOX", "COPYTO 0", "INBOX", "SUB 0", "OUTBOX"),
            parse_input_data("b a"))
        out = capsys.readouterr()[0]
        assert out == "-1\n"

    def test_adder_int_char(self, capsys):
        """
        An adder will not add an integer and a character.
        """
        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "INBOX", "ADD 0", "OUTBOX"),
                parse_input_data("1 b"))
        out = capsys.readouterr()[0]
        assert out == ""

    def test_subber_int_char(self, capsys):
        """
        A subber will not sub an integer and a character.
        """
        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "INBOX", "SUB 0", "OUTBOX"),
                parse_input_data("a 2"))
        out = capsys.readouterr()[0]
        assert out == ""

    def test_subber_char_int(self, capsys):
        """
        A subber will not sub a character and an integer.
        """
        with pytest.raises(IllegalOperation):
            mainloop(
                program("INBOX", "COPYTO 0", "INBOX", "SUB 0", "OUTBOX"),
                parse_input_data("1 b"))
        out = capsys.readouterr()[0]
        assert out == ""
