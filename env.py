"""
env.py - Environment variable management

The shell maintains its own copy of the environment. When a child process
is spawned, it inherits a copy of this environment.

In Python, os.environ gives you the current process's environment.
We wrap it here so the rest of the shell has a clean interface for
getting, setting, and removing variables.

Concepts to research:
  - os.environ (it behaves like a dict)
  - os.environ.copy() - snapshot of current environment
  - Environment variable inheritance (child processes get a copy)
  - The difference between shell variables and exported variables
    (in bash: FOO=bar sets a shell var; export FOO=bar makes it inherited)
    For simplicity, you can treat all variables as exported.
"""

import os


class Env:
    def __init__(self):
        # Start with a copy of the current process environment.
        # This gives your shell all the variables that were set when
        # you launched it (PATH, HOME, USER, etc.)
        self._env: dict[str, str] = os.environ.copy()

        # Store the previous working directory for "cd -"
        self._prev_dir: str | None = None

    def get(self, key: str, default: str | None = None) -> str | None:
        """Get an environment variable by name."""
        return self._env.get(key, default)

    def set(self, key: str, value: str) -> None:
        """
        Set an environment variable.
        Also update os.environ so subprocesses inherit it.
        """
        # TODO: set in self._env and os.environ
        self._env[key] = value
        os.environ[key] = value
        pass

    def unset(self, key: str) -> None:
        """
        Remove an environment variable.
        Also remove from os.environ.
        Handle the case where key doesn't exist.
        """
        # TODO: remove from self._env and os.environ (use .pop with default)
        self._env.pop(key, None)
        os.environ.pop(key, None)
        pass

    def get_env(self) -> dict[str, str]:
        """
        Return the full environment dict.
        Used by executor.py when spawning subprocesses.
        """
        return self._env.copy()

    def get_prev_dir(self) -> str | None:
        """Return the previous working directory (for cd -)."""
        return self._prev_dir

    def set_prev_dir(self, path: str) -> None:
        """Store the current directory before a cd (for cd -)."""
        self._prev_dir = path

    def expand(self, value: str) -> str:
        """
        Expand environment variables in a string.

        Examples:
          "$HOME/projects"  ->  "/home/user/projects"
          "$USER"           ->  "neo"
          "hello"           ->  "hello"  (unchanged)

        Hint: os.path.expandvars(value) does this for you using os.environ.
        Since we manage our own env dict, you might want to temporarily
        update os.environ or implement your own expansion.

        Simple implementation: use a regex to find $VAR patterns and
        replace them with self._env.get(VAR, "").

        Concepts to research:
          - os.path.expandvars()
          - re.sub() with a function as the replacement
        """
        # TODO: implement variable expansion

        import re

        def replace(match):
            key = match.group(1) or match.group(2)
            return self._env.get(key, "")

        return re.sub(r"\$\{(\w+)\}|\$(\w+)", replace, value)
