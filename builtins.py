"""
builtins.py - Built-in shell commands

Some commands CANNOT be implemented as external programs. They need to
be built into the shell itself because they affect the shell's own state.

The classic example is `cd`. If `cd` were an external program, it would
change the working directory of the child process, but when that child
exits, the shell's own working directory would be unchanged. Useless.

So `cd` has to run inside the shell process using os.chdir().

Similarly, `exit` has to set shell.running = False — an external program
can't do that.

Builtins to implement:
  - cd      change working directory
  - exit    quit the shell
  - echo    print arguments to stdout
  - export  set an environment variable
  - unset   remove an environment variable
  - env     print all environment variables
  - history print command history
  - help    print available builtins

Concepts to research:
  - os.chdir() and os.getcwd()
  - os.environ
  - Why cd, exit, export must be builtins (not external processes)
"""

import os
import sys
from env import Env
from history import History


class Builtins:
    def __init__(self, env: Env, history: History):
        self.env = env
        self.history = history

        # Registry mapping command names to their handler methods.
        # This is a clean pattern — instead of a long if/elif chain,
        # you look up the handler in this dict and call it.
        self.commands: dict = {
            "cd": self.cd,
            "exit": self.exit,
            "echo": self.echo,
            "export": self.export,
            "unset": self.unset,
            "env": self.env_cmd,
            "history": self.history_cmd,
            "help": self.help,
        }

    def is_builtin(self, name: str) -> bool:
        """Returns True if the given command name is a builtin."""
        return name in self.commands

    def run(self, name: str, args: list[str]) -> int:
        """
        Runs a builtin command and returns its exit code.
        Looks up the handler in self.commands and calls it with args.
        Returns 1 if the command is not found (shouldn't happen if
        you check is_builtin first, but be safe).
        """
        handler = self.commands.get(name)
        if handler:
            return handler(args)
        return 1

    def cd(self, args: list[str]) -> int:
        """
        Change the current working directory.

        Behavior to implement:
          - cd          -> go to home directory (os.path.expanduser("~"))
          - cd ~        -> same as above
          - cd -        -> go to previous directory (store it in self.env)
          - cd <path>   -> go to that path
          - cd too many args -> print error

        Use os.chdir(path) to change directory.
        Handle FileNotFoundError and NotADirectoryError.

        Hint: store the previous directory before changing so cd - works.
        """
        # TODO: implement cd
        return 0

    def exit(self, args: list[str]) -> int:
        """
        Exit the shell.

        Behavior:
          - exit      -> exit with code 0
          - exit <n>  -> exit with code n (must be an integer)

        Hint: you need a way to tell the Shell to stop its REPL loop.
        One clean way: raise a custom exception like ShellExit(code)
        and catch it in shell.py's run() loop.
        Another way: call sys.exit(code) directly.

        sys.exit() raises SystemExit which you can catch if needed.
        """
        # TODO: implement exit
        return 0

    def echo(self, args: list[str]) -> int:
        """
        Print arguments to stdout.

        Behavior:
          - echo hello world   -> "hello world"
          - echo -n hello      -> "hello" (no trailing newline)
          - echo $HOME         -> variable expansion (optional for now,
                                  note that the shell should expand $VARS
                                  before they get here ideally)

        Hint: ' '.join(args) joins a list with spaces between.
        print() adds a newline by default; use end="" to suppress it.
        """
        # TODO: implement echo
        return 0

    def export(self, args: list[str]) -> int:
        """
        Set an environment variable.

        Behavior:
          - export FOO=bar    -> set FOO to "bar"
          - export FOO        -> mark FOO as exported (if already set)
          - export            -> print all exported variables

        Variables set with export are inherited by child processes.

        Hint: parse "FOO=bar" by splitting on the first "=" only:
          key, value = arg.split("=", 1)
        """
        # TODO: implement export
        return 0

    def unset(self, args: list[str]) -> int:
        """
        Remove an environment variable.

        Behavior:
          - unset FOO    -> remove FOO from the environment
          - unset FOO BAR -> remove multiple variables

        Use self.env.unset(key) — you'll implement that in env.py.
        """
        # TODO: implement unset
        return 0

    def env_cmd(self, args: list[str]) -> int:
        """
        Print all current environment variables.
        Format: KEY=value (one per line), sorted alphabetically.
        """
        # TODO: print all env vars
        return 0

    def history_cmd(self, args: list[str]) -> int:
        """
        Print command history.

        Behavior:
          - history       -> print all history with line numbers
          - history <n>   -> print last n entries
          - history -c    -> clear history

        Format:
          1  ls -la
          2  cd /tmp
          3  echo hello
        """
        # TODO: implement history display
        return 0

    def help(self, args: list[str]) -> int:
        """
        Print available builtin commands.
        Just iterate self.commands.keys() and print them.
        Optionally print a short description for each.
        """
        print("pysh builtins:")
        for name in sorted(self.commands.keys()):
            print(f"  {name}")
        return 0
