"""
parser.py - Turns a list of tokens into structured command objects

The parser is the second stage. It takes the flat list of tokens from
the lexer and builds meaningful structures from them.

For example, tokens for:
    ls -la | grep foo > output.txt

Would be parsed into a Pipeline containing two Commands:
    Pipeline([
        Command(name="ls", args=["-la"]),
        Command(name="grep", args=["foo"], redirect_out="output.txt")
    ])

This is where the grammar of your shell lives. Start simple and add
complexity (semicolons, subshells, etc.) as you go.

Concepts to research:
  - What is a parser / AST (Abstract Syntax Tree)?
  - Recursive descent parsing (you won't need this for a simple shell,
    but it's worth knowing the term)
  - Python dataclasses — a clean way to define Command and Pipeline
"""

from dataclasses import dataclass, field
from lexer import Token


@dataclass
class Command:
    """
    Represents a single command to be executed.

    name         - the executable name, e.g. "ls", "grep", "echo"
    args         - list of arguments, e.g. ["-la", "/tmp"]
    redirect_in  - filename to read stdin from, e.g. "input.txt" for <
    redirect_out - filename to write stdout to, e.g. "output.txt" for >
    redirect_append - filename to append stdout to, e.g. "output.txt" for >>

    Example:
      "grep -i foo < input.txt > output.txt"
      Command(name="grep", args=["-i", "foo"],
              redirect_in="input.txt", redirect_out="output.txt")
    """
    name: str
    args: list[str] = field(default_factory=list)
    redirect_in: str | None = None
    redirect_out: str | None = None
    redirect_append: str | None = None


@dataclass
class Pipeline:
    """
    Represents one or more commands connected by pipes.

    commands - list of Command objects, in order left to right
    If there's only one command and no pipes, this still wraps it
    in a Pipeline for consistency — the executor always gets a Pipeline.

    Example:
      "ls | grep foo | wc -l"
      Pipeline([
          Command("ls"),
          Command("grep", args=["foo"]),
          Command("wc", args=["-l"])
      ])
    """
    commands: list[Command] = field(default_factory=list)


class Parser:
    def parse(self, tokens: list[Token]) -> list[Pipeline]:
        """
        Takes a list of tokens and returns a list of Pipelines.

        It's a list of Pipelines (not just one) because the user can
        run multiple commands separated by semicolons:
            ls ; echo done ; pwd
        Each semicolon-separated group becomes its own Pipeline.

        Approach:
          1. Split the token list on SEMICOLON tokens into groups
          2. For each group, call _parse_pipeline()
          3. Return the list of resulting Pipelines

        Hint: if there are no semicolons, you still return a list,
        just with one Pipeline in it.
        """
        # TODO: split on SEMICOLON, parse each group as a pipeline
        return []

    def _parse_pipeline(self, tokens: list[Token]) -> Pipeline:
        """
        Takes a list of tokens (no semicolons) and returns a Pipeline.

        Approach:
          1. Split the token list on PIPE tokens into groups
          2. For each group, call _parse_command()
          3. Return a Pipeline containing all the Commands

        Example tokens for "ls -la | grep foo":
          [WORD:ls, WORD:-la, PIPE:|, WORD:grep, WORD:foo]
        Split on PIPE:
          [[WORD:ls, WORD:-la], [WORD:grep, WORD:foo]]
        Parse each:
          [Command("ls", ["-la"]), Command("grep", ["foo"])]
        """
        # TODO: split on PIPE tokens and parse each segment as a command
        return Pipeline()

    def _parse_command(self, tokens: list[Token]) -> Command:
        """
        Takes a list of WORD/REDIRECT tokens and returns a Command.

        The first WORD token is always the command name.
        Subsequent WORD tokens are arguments — UNLESS the previous
        token was a redirect operator, in which case this WORD is
        the filename for that redirect.

        Walk the tokens and build up the Command:
          - First token -> command name
          - REDIRECT_OUT followed by WORD -> set redirect_out to that word
          - REDIRECT_APPEND followed by WORD -> set redirect_append
          - REDIRECT_IN followed by WORD -> set redirect_in
          - Any other WORD -> append to args

        Hint: use an index-based loop (for i, token in enumerate(tokens))
        so you can look ahead at tokens[i+1] when you hit a redirect.
        """
        # TODO: implement command parsing
        return Command(name="")
