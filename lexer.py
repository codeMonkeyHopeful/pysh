"""
lexer.py - Tokenizes raw input strings into a list of tokens

The lexer is the first stage of processing a command. It takes a raw
string like:

    echo "hello world" | grep -i hello > output.txt

and breaks it into meaningful tokens:

    ["echo", "hello world", "|", "grep", "-i", "hello", ">", "output.txt"]

Notice that "hello world" becomes a single token — the lexer understands
that quotes group words together.

This is called "lexical analysis" or "tokenization" and is the first stage
of almost every language parser, compiler, or interpreter ever written.

Concepts to research:
  - What is a lexer / tokenizer?
  - Python's shlex module (this does a lot of the work for you — try it first,
    then consider writing your own once you understand what it does)
  - Handling single quotes vs double quotes (they behave differently in bash)
  - What characters are "special" in a shell (|, >, <, &, ;)
"""


class Token:
    """
    Represents a single token from the input.

    type  - what kind of token this is (see TokenType below)
    value - the actual string value

    Example:
      Token(type="WORD", value="echo")
      Token(type="PIPE", value="|")
      Token(type="REDIRECT_OUT", value=">")
    """

    # Token types
    WORD = "WORD"               # a regular word or argument
    PIPE = "PIPE"               # |
    REDIRECT_OUT = "REDIRECT_OUT"   # >
    REDIRECT_APPEND = "REDIRECT_APPEND"  # >>
    REDIRECT_IN = "REDIRECT_IN"     # <
    SEMICOLON = "SEMICOLON"     # ; (run commands sequentially)

    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


class Lexer:
    def tokenize(self, raw_input: str) -> list[Token]:
        """
        Takes a raw input string and returns a list of Token objects.

        Approach:
          1. Start with Python's shlex.split() to handle basic splitting
             and quote handling — import shlex and call shlex.split(raw_input)
          2. Walk through the resulting list and convert special characters
             (|, >, >>, <, ;) into their corresponding Token types
          3. Everything else is a WORD token

        Edge cases to handle:
          - Empty string -> return []
          - ">" vs ">>" (redirect vs append) — check for >> first
          - Quoted strings should be a single WORD token with quotes stripped
          - What happens with shlex and unclosed quotes? Handle the exception.

        Hint: shlex.split() raises ValueError on unclosed quotes.
        Catch it and either raise a friendlier error or return [].
        """
        # TODO: implement tokenization
        # Starter hint:
        #   import shlex
        #   parts = shlex.split(raw_input)  # handles quotes for you
        #   then walk parts and classify each as a Token
        return []
