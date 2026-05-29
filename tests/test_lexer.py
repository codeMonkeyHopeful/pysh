"""
tests/test_lexer.py - Tests for lexer.py

Run with: pytest tests/test_lexer.py -v
"""

import pytest
from lexer import Lexer, Token


@pytest.fixture
def lexer():
    return Lexer()


def token_types(tokens):
    """Helper: extract just the types from a token list."""
    return [t.type for t in tokens]


def token_values(tokens):
    """Helper: extract just the values from a token list."""
    return [t.value for t in tokens]


class TestBasicWords:
    def test_single_word(self, lexer):
        tokens = lexer.tokenize("ls")
        assert len(tokens) == 1
        assert tokens[0].type == Token.WORD
        assert tokens[0].value == "ls"

    def test_multiple_words(self, lexer):
        tokens = lexer.tokenize("ls -la /tmp")
        assert token_values(tokens) == ["ls", "-la", "/tmp"]
        assert all(t.type == Token.WORD for t in tokens)

    def test_empty_string(self, lexer):
        tokens = lexer.tokenize("")
        assert tokens == []

    def test_whitespace_only(self, lexer):
        tokens = lexer.tokenize("   ")
        assert tokens == []


class TestQuotes:
    def test_double_quoted_string(self, lexer):
        """Double quotes should group words into a single token."""
        tokens = lexer.tokenize('echo "hello world"')
        assert len(tokens) == 2
        assert tokens[1].value == "hello world"

    def test_single_quoted_string(self, lexer):
        """Single quotes should group words into a single token."""
        tokens = lexer.tokenize("echo 'hello world'")
        assert len(tokens) == 2
        assert tokens[1].value == "hello world"

    def test_quoted_string_with_special_chars(self, lexer):
        """Special chars inside quotes should be treated as plain text."""
        tokens = lexer.tokenize('echo "hello | world"')
        assert len(tokens) == 2
        assert tokens[1].value == "hello | world"


class TestPipe:
    def test_single_pipe(self, lexer):
        tokens = lexer.tokenize("ls | grep foo")
        assert Token.PIPE in token_types(tokens)

    def test_pipe_position(self, lexer):
        tokens = lexer.tokenize("ls | grep foo")
        assert tokens[1].type == Token.PIPE

    def test_multiple_pipes(self, lexer):
        tokens = lexer.tokenize("ls | grep foo | wc -l")
        pipes = [t for t in tokens if t.type == Token.PIPE]
        assert len(pipes) == 2


class TestRedirects:
    def test_redirect_out(self, lexer):
        tokens = lexer.tokenize("ls > output.txt")
        assert Token.REDIRECT_OUT in token_types(tokens)
        # filename should follow
        idx = token_types(tokens).index(Token.REDIRECT_OUT)
        assert tokens[idx + 1].value == "output.txt"

    def test_redirect_append(self, lexer):
        tokens = lexer.tokenize("echo hello >> output.txt")
        assert Token.REDIRECT_APPEND in token_types(tokens)

    def test_redirect_in(self, lexer):
        tokens = lexer.tokenize("cat < input.txt")
        assert Token.REDIRECT_IN in token_types(tokens)

    def test_redirect_append_not_confused_with_redirect_out(self, lexer):
        """>> should be REDIRECT_APPEND, not two REDIRECT_OUT tokens."""
        tokens = lexer.tokenize("echo hello >> file.txt")
        types = token_types(tokens)
        assert Token.REDIRECT_APPEND in types
        assert types.count(Token.REDIRECT_OUT) == 0


class TestSemicolon:
    def test_semicolon(self, lexer):
        tokens = lexer.tokenize("echo hello ; echo world")
        assert Token.SEMICOLON in token_types(tokens)

    def test_multiple_semicolons(self, lexer):
        tokens = lexer.tokenize("echo a ; echo b ; echo c")
        semis = [t for t in tokens if t.type == Token.SEMICOLON]
        assert len(semis) == 2


class TestComplex:
    def test_full_pipeline_with_redirect(self, lexer):
        """ls -la | grep foo > output.txt"""
        tokens = lexer.tokenize("ls -la | grep foo > output.txt")
        types = token_types(tokens)
        assert Token.PIPE in types
        assert Token.REDIRECT_OUT in types
        assert token_values(tokens)[0] == "ls"

    def test_unclosed_quote_does_not_crash(self, lexer):
        """Unclosed quote should return [] or raise a clean error, not crash."""
        try:
            result = lexer.tokenize('echo "unclosed')
            assert result == []
        except ValueError:
            pass  # also acceptable
