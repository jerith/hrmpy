import pytest

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
