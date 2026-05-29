"""
main.py - Entry point for pysh

This is the first file that runs. It creates the Shell instance and
starts the REPL (Read-Eval-Print Loop). Keep this file thin — its only
job is to bootstrap and hand off to shell.py.
"""

from shell import Shell


def main():
    shell = Shell()
    shell.run()


if __name__ == "__main__":
    main()
