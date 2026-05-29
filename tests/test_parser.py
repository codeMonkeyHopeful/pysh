"""
tests/test_parser.py - Tests for parser.py

Run with: pytest tests/test_parser.py -v
"""

import pytest
from lexer import Lexer, Token
from parser import Parser, Command, Pipeline


@pytest.fixture
def parser():
    return Parser()


@pytest.fixture
def lexer():
    return Lexer()


def parse(input_str):
    """Helper: lex and parse a string in one step."""
    tokens = Lexer().tokenize(input_str)
    return Parser().parse(tokens)


class TestSingleCommand:
    def test_simple_command(self):
        pipelines = parse("ls")
        assert len(pipelines) == 1
        assert len(pipelines[0].commands) == 1
        assert pipelines[0].commands[0].name == "ls"

    def test_command_with_args(self):
        pipelines = parse("ls -la /tmp")
        cmd = pipelines[0].commands[0]
        assert cmd.name == "ls"
        assert cmd.args == ["-la", "/tmp"]

    def test_empty_input(self):
        pipelines = parse("")
        assert pipelines == []


class TestRedirects:
    def test_redirect_out(self):
        pipelines = parse("ls > output.txt")
        cmd = pipelines[0].commands[0]
        assert cmd.redirect_out == "output.txt"
        assert "output.txt" not in cmd.args

    def test_redirect_append(self):
        pipelines = parse("echo hello >> output.txt")
        cmd = pipelines[0].commands[0]
        assert cmd.redirect_append == "output.txt"

    def test_redirect_in(self):
        pipelines = parse("cat < input.txt")
        cmd = pipelines[0].commands[0]
        assert cmd.redirect_in == "input.txt"
        assert "input.txt" not in cmd.args

    def test_redirect_does_not_appear_in_args(self):
        """The redirect filename should not also appear in args."""
        pipelines = parse("grep foo < input.txt > output.txt")
        cmd = pipelines[0].commands[0]
        assert "input.txt" not in cmd.args
        assert "output.txt" not in cmd.args
        assert cmd.redirect_in == "input.txt"
        assert cmd.redirect_out == "output.txt"


class TestPipeline:
    def test_single_pipe(self):
        pipelines = parse("ls | grep foo")
        assert len(pipelines) == 1
        assert len(pipelines[0].commands) == 2
        assert pipelines[0].commands[0].name == "ls"
        assert pipelines[0].commands[1].name == "grep"

    def test_pipe_args(self):
        pipelines = parse("ls -la | grep foo")
        assert pipelines[0].commands[0].args == ["-la"]
        assert pipelines[0].commands[1].args == ["foo"]

    def test_multiple_pipes(self):
        pipelines = parse("ls | grep foo | wc -l")
        assert len(pipelines[0].commands) == 3

    def test_pipe_with_redirect_on_last(self):
        """ls | grep foo > output.txt — redirect applies to last command."""
        pipelines = parse("ls | grep foo > output.txt")
        commands = pipelines[0].commands
        assert commands[-1].redirect_out == "output.txt"
        assert commands[0].redirect_out is None


class TestSemicolon:
    def test_two_commands(self):
        pipelines = parse("echo hello ; echo world")
        assert len(pipelines) == 2
        assert pipelines[0].commands[0].name == "echo"
        assert pipelines[1].commands[0].name == "echo"

    def test_three_commands(self):
        pipelines = parse("echo a ; echo b ; echo c")
        assert len(pipelines) == 3

    def test_semicolon_with_pipeline(self):
        """ls | grep foo ; echo done — two pipelines."""
        pipelines = parse("ls | grep foo ; echo done")
        assert len(pipelines) == 2
        assert len(pipelines[0].commands) == 2
        assert len(pipelines[1].commands) == 1


class TestCommandDataclass:
    def test_command_defaults(self):
        """Command should have sensible defaults."""
        cmd = Command(name="ls")
        assert cmd.args == []
        assert cmd.redirect_in is None
        assert cmd.redirect_out is None
        assert cmd.redirect_append is None

    def test_pipeline_defaults(self):
        """Pipeline should default to empty commands list."""
        p = Pipeline()
        assert p.commands == []
