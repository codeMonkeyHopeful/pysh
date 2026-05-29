"""
history.py - Command history with file persistence

Every command the user runs gets saved to history. This lets them:
  - Press up arrow to cycle through previous commands
  - Run `history` to see all past commands
  - Optionally: use Ctrl+R for reverse search (advanced)

History is persisted to a file (~/.pysh_history) so it survives
between sessions — just like bash's ~/.bash_history.

Concepts to research:
  - Python's readline module (handles up-arrow history for free!)
  - File I/O (open, read, write, append mode)
  - os.path.expanduser("~") to get the home directory
  - atexit module — register a function to run when Python exits
    (useful for saving history on exit automatically)
"""

import os
import readline
import atexit

HISTORY_FILE = os.path.expanduser("~/.pysh_history")
MAX_HISTORY = 1000


class History:
    def __init__(self):
        self._entries: list[str] = []
        self._setup_readline()

    def _setup_readline(self):
        """
        Configure readline for history support.

        readline is a Python module wrapping GNU readline. Once configured,
        it automatically handles:
          - Up/down arrow keys to cycle through history
          - Ctrl+R for reverse search
          - Tab completion (if you configure a completer)

        Steps:
          1. Load history from HISTORY_FILE if it exists
             (readline.read_history_file)
          2. Set the max history length
             (readline.set_history_length)
          3. Register save_to_file to run on exit
             (atexit.register)

        Hint: wrap readline.read_history_file in try/except FileNotFoundError
        since the file won't exist on first run.
        """
        # TODO: load history file, set history length, register atexit save

        if os.path.exists(HISTORY_FILE):
            readline.read_history_file(HISTORY_FILE)
            readline.set_history_length(MAX_HISTORY)
            self._entries = readline.get_history_item(
                1, readline.get_current_history_length() + 1
            )
        readline.set_history_length(MAX_HISTORY)

        atexit.register(self.save_to_file)

        pass

    def add(self, command: str) -> None:
        """
        Add a command to history.

        Behavior:
          - Don't add empty strings
          - Don't add duplicates of the immediately previous command
            (bash does this by default — running ls twice only adds it once)
          - Add to self._entries
          - Also add to readline's history with readline.add_history()
            so up-arrow works immediately

        Hint: check self._entries[-1] if len(self._entries) > 0
        """
        # TODO: implement add

        if (
            command
            and (not self._entries or command != self._entries[-1])
            and len(command.strip()) > 0
        ):
            self._entries.append(command)
            readline.add_history(command)
        pass

    def get_all(self) -> list[str]:
        """Return all history entries."""
        return self._entries.copy()

    def get_last(self, n: int) -> list[str]:
        """Return the last n history entries."""
        return self._entries[-n:]

    def clear(self) -> None:
        """
        Clear all history.
        Also clear readline's history with readline.clear_history().
        """
        # TODO: clear self._entries and readline history
        self._entries = []
        readline.clear_history()
        pass

    def save_to_file(self) -> None:
        """
        Save history to HISTORY_FILE.

        Use readline.write_history_file(HISTORY_FILE) — readline handles
        the file format for you.

        Wrap in try/except in case the file isn't writable.
        """
        # TODO: save history file
        pass

    def __len__(self) -> int:
        return len(self._entries)
