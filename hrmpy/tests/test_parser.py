import pytest

from hrmpy import parser


def test_parse_program_empty():
    with pytest.raises(RuntimeError):
        parser.parse_program("")


def test_parse_program_no_header():
    with pytest.raises(RuntimeError):
        parser.parse_program("\n".join([
            "INBOX",
            "OUTBOX",
        ]))


def test_parse_program_header_only():
    ops = parser.parse_program("-- HUMAN RESOURCE MACHINE PROGRAM --")
    assert ops == []
