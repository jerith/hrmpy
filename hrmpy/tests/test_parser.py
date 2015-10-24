import pytest

from hrmpy.operations import Integer, Character
from hrmpy import parser


class TestParseProgram(object):

    def test_empty_program(self):
        """
        An empty string is not a program.
        """
        with pytest.raises(RuntimeError):
            parser.parse_program("")

    def test_no_header(self):
        """
        A program without a header is not a program.
        """
        with pytest.raises(RuntimeError):
            parser.parse_program("\n".join([
                "INBOX",
                "OUTBOX",
            ]))

    def test_header_only(self):
        """
        A header on its own is an empty program.
        """
        ops = parser.parse_program("-- HUMAN RESOURCE MACHINE PROGRAM --")
        assert ops == []

    def test_header_after_nonsense(self):
        """
        Anything before the header is ignored.
        """
        ops = parser.parse_program("\n".join([
            "This is an empty program.",
            "",
            "It is my empty program, but you can have it if you want.",
            "-- HUMAN RESOURCE MACHINE PROGRAM --",
        ]))
        assert ops == []

    def test_small_program(self):
        """
        A header followed by instructions is a valid program.
        """
        ops = parser.parse_program("\n".join([
            "-- HUMAN RESOURCE MACHINE PROGRAM --",
            "INBOX",
            "OUTBOX",
        ]))
        assert map(str, ops) == ['INBOX', 'OUTBOX']

    def test_small_program_after_nonsense(self):
        """
        A program can include documentation or whatever before the header.
        """
        ops = parser.parse_program("\n".join([
            "This is a small program that copies a single value from input",
            "to output.",
            "",
            "-- HUMAN RESOURCE MACHINE PROGRAM --",
            "INBOX",
            "OUTBOX",
        ]))
        assert map(str, ops) == ['INBOX', 'OUTBOX']

    def test_memset(self):
        """
        A program can include some initial memory values.
        """
        ops = parser.parse_program("\n".join([
            "-- HUMAN RESOURCE MACHINE PROGRAM --",
            "COPYFROM 0",
            "OUTBOX",
            "COPYFROM 1",
            "OUTBOX",
            ".memset 0 1",
            ".memset 1 a",
        ]))
        assert map(str, ops) == [
            'COPYFROM 0', 'OUTBOX', 'COPYFROM 1', 'OUTBOX',
            '.memset 0 1', '.memset 1 a']

    def test_addresses(self):
        """
        A memory operation can use direct or indirect addressing.
        """
        ops = parser.parse_program("\n".join([
            "-- HUMAN RESOURCE MACHINE PROGRAM --",
            "COPYFROM [0]",
            "OUTBOX",
            "COPYFROM 1",
            "OUTBOX",
            ".memset 0 2",
            ".memset 1 a",
            ".memset 2 b",
        ]))
        assert map(str, ops) == [
            'COPYFROM [0]', 'OUTBOX', 'COPYFROM 1', 'OUTBOX',
            '.memset 0 2', '.memset 1 a', '.memset 2 b']


class TestParseInput(object):

    def test_empty_input(self):
        """
        An empty string is empty input.
        """
        input_data = parser.parse_input_data("")
        assert input_data == []

    def test_some_numbers(self):
        """
        A space-separated string containing numbers is valid input.
        """
        input_data = parser.parse_input_data("1 2 3")
        assert input_data == [Integer(1), Integer(2), Integer(3)]

    def test_big_numbers(self):
        """
        A space-separated string containing long numbers is valid input.
        """
        input_data = parser.parse_input_data("123 -37")
        assert input_data == [Integer(123), Integer(-37)]

    def test_some_characters(self):
        """
        A space-separated string containing characters is valid input.
        """
        input_data = parser.parse_input_data("a b c")
        assert input_data == [
            Character('a'), Character('b'), Character('c')]

    def test_mixed_input(self):
        """
        A space-separated string containing numbers and characters is valid.
        """
        input_data = parser.parse_input_data("1 2 a b 3")
        assert input_data == [
            Integer(1), Integer(2), Character('a'), Character('b'), Integer(3)]
