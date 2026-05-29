"""
executor.py - Executes parsed command pipelines

This is the most complex and most interesting module. It's where you
interact directly with the operating system to actually run commands,
set up pipes between them, and handle file redirects.

This is where you'll learn the most about how shells actually work.

Key OS concepts you'll need to research:
  - os.fork()      - creates a copy of the current process (parent + child)
  - os.execvp()    - replaces the current process with a new program
  - os.pipe()      - creates a (read_fd, write_fd) pair for IPC
  - os.dup2()      - redirects one file descriptor to another
  - os.waitpid()   - waits for a child process to finish
  - os.open()      - opens a file and returns a file descriptor

OR the higher-level approach:
  - subprocess.Popen() - Python's wrapper around fork/exec
  - stdin/stdout/stderr parameters on Popen
  - subprocess.PIPE

Start with subprocess.Popen for your first implementation — it's easier
to get working. Once it works, try rewriting with os.fork/execvp to
understand what Popen is doing under the hood.

File descriptors (fds):
  0 = stdin  (read from keyboard by default)
  1 = stdout (write to terminal by default)
  2 = stderr (write to terminal by default)

Pipes work by connecting stdout of process A to stdin of process B.
os.pipe() gives you two fds: (read_end, write_end).
You give write_end to process A as its stdout,
and read_end to process B as its stdin.
"""

import os
import subprocess
from parser import Pipeline, Command
from env import Env


class Executor:
    def __init__(self, env: Env):
        self.env = env

    def execute(self, pipeline: Pipeline) -> int:
        """
        Executes a full pipeline and returns the exit code of the
        last command in the pipeline.

        If there's only one command, just run it directly.
        If there are multiple commands, set up pipes between them.

        Returns the exit code (0 = success, non-zero = error).
        The exit code is useful for features like $? later.
        """
        if not pipeline.commands:
            return 0

        if len(pipeline.commands) == 1:
            return self._execute_single(pipeline.commands[0])
        else:
            return self._execute_pipeline(pipeline.commands)

    def _execute_single(self, command: Command) -> int:
        """
        Executes a single command (no pipes) with optional redirects.

        Steps:
          1. Build the full argv list: [command.name] + command.args
          2. Set up stdin/stdout based on redirects:
             - redirect_in  -> open file for reading, use as stdin
             - redirect_out -> open file for writing, use as stdout
             - redirect_append -> open file for appending, use as stdout
          3. Spawn the process with subprocess.Popen
          4. Wait for it to finish and return the exit code
          5. Close any file handles you opened

        Don't forget to handle FileNotFoundError — this is what happens
        when the command doesn't exist (e.g. the user types a typo).
        Print something like "pysh: command not found: <name>"

        Hint for subprocess.Popen:
          proc = subprocess.Popen(
              argv,
              stdin=stdin_file,    # None means inherit from shell
              stdout=stdout_file,  # None means inherit from shell
              env=self.env.get_env()
          )
          return proc.wait()
        """
        # TODO: implement single command execution with redirects
        return 0

    def _execute_pipeline(self, commands: list[Command]) -> int:
        """
        Executes multiple commands connected by pipes.

        This is the hardest part. The key insight:
          - For N commands you need N-1 pipes
          - Each pipe connects stdout of command[i] to stdin of command[i+1]

        Approach using subprocess.Popen:
          1. Create a list to hold all the Popen objects
          2. For the first command:
             - stdin = handle redirects or None
             - stdout = subprocess.PIPE (we'll connect it to next command)
          3. For middle commands:
             - stdin = previous process's stdout
             - stdout = subprocess.PIPE
          4. For the last command:
             - stdin = previous process's stdout
             - stdout = handle redirects or None
          5. Wait for all processes to finish
          6. Return exit code of the last process

        Hint: subprocess.Popen has a stdout attribute once created.
        You can pass proc.stdout as the stdin of the next Popen call.

        Concepts to research:
          - subprocess.PIPE
          - Why you need to be careful about closing pipe ends
            (google: "subprocess pipe deadlock python")
        """
        # TODO: implement pipeline execution
        return 0
