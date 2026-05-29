"""
shell.py - The Shell class that wires everything together

This is the heart of the shell. It owns the REPL loop and coordinates
between all the other modules. Think of it as the conductor — it doesn't
do the work itself, it delegates to the right module at the right time.

REPL stands for Read-Eval-Print Loop:
  Read   -> get input from the user
  Eval   -> parse and execute it
  Print  -> show the result (the command handles this, not us)
  Loop   -> do it again

Concepts to research:
  - Python's input() vs readline module
  - try/except for KeyboardInterrupt (Ctrl+C) and EOFError (Ctrl+D)
  - What it means for a shell to have "state" (cwd, env, history)
"""

import os
from lexer import Lexer
from parser import Parser
from executor import Executor
from builtins import Builtins
from env import Env
from history import History


class Shell:
    def __init__(self):
        self.env = Env()
        self.history = History()
        self.lexer = Lexer()
        self.parser = Parser()
        self.executor = Executor(self.env)
        self.builtins = Builtins(self.env, self.history)
        self.running = True

    def run(self):
        """
        The main REPL loop. Keeps running until self.running is False
        or the user hits Ctrl+D (EOF).

        Loop structure:
          1. Print the prompt
          2. Read a line of input
          3. Handle empty input (just hit enter — do nothing)
          4. Add input to history
          5. Lex -> Parse -> Execute
          6. Handle errors without crashing the shell

        Things to handle gracefully:
          - KeyboardInterrupt (Ctrl+C): print a newline, continue the loop
          - EOFError (Ctrl+D): print "exit", break the loop
          - Any exception from execution: print the error, continue the loop
            (a real shell never crashes — it just shows an error)
        """
        while self.running:
            try:
                # TODO: get the prompt string from _get_prompt()
                # TODO: read input with input() or readline
                # TODO: skip empty lines
                # TODO: add to history
                # TODO: lex the raw input into tokens
                # TODO: parse the tokens into a command structure
                # TODO: check if the command is a builtin, if so run it
                # TODO: otherwise pass to executor
                pass
            except KeyboardInterrupt:
                # TODO: print a newline and continue
                pass
            except EOFError:
                # TODO: print "exit" and break
                pass

    def _get_prompt(self) -> str:
        """
        Build the prompt string shown to the user before each input.
        A basic prompt might look like: /home/user/projects/pysh $

        Concepts to research:
          - os.getcwd() to get current working directory
          - String formatting / f-strings
          - ANSI escape codes if you want to add color (optional but fun)
            e.g. \033[94m for blue, \033[0m to reset

        Hint: real shells use $PS1 environment variable for the prompt.
        You could support that too once the basics work.
        """
        # TODO: return a formatted prompt string showing current directory
        return "$ "
