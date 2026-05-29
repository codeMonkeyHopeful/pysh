# pysh 🐚

A shell built in Python. A learning project covering lexing, parsing,
process management, pipes, redirects, and OS fundamentals.

## Project Structure

```
pysh/
├── main.py       # Entry point — boots the shell
├── shell.py      # Shell class — owns the REPL loop
├── lexer.py      # Stage 1: raw string → list of tokens
├── parser.py     # Stage 2: tokens → structured command objects
├── executor.py   # Stage 3: runs commands, sets up pipes/redirects
├── builtins.py   # Built-in commands (cd, exit, echo, export, history)
├── env.py        # Environment variable management
└── history.py    # Command history + readline integration
```

## How to run

```bash
python main.py
```

## Recommended implementation order

Work through the files in this order — each one builds on the last:

1. **`env.py`** — Start here. Simple get/set/unset with no dependencies.

2. **`history.py`** — Also simple. Get readline working so up-arrow works
   early. Very satisfying.

3. **`lexer.py`** — Tokenize raw input. Use `shlex` to handle quotes,
   then classify special characters as their token types.

4. **`parser.py`** — Turn tokens into `Command` and `Pipeline` objects.
   Work through `_parse_command` first, then `_parse_pipeline`,
   then `parse`.

5. **`shell.py`** — Implement `_get_prompt` and the REPL loop in `run`.
   At this point you can wire everything together even before executor
   works — just print the parsed commands to verify your lexer/parser.

6. **`builtins.py`** — Implement `cd` and `exit` first (most important),
   then `echo`, `export`, `env_cmd`, `history_cmd`.

7. **`executor.py`** — The hardest part. Start with `_execute_single`
   (no pipes, just basic execution + redirects), get that working,
   then tackle `_execute_pipeline`.

## Milestone checklist

- [ ] `python main.py` starts without errors
- [ ] Prompt shows current directory
- [ ] `echo hello world` works
- [ ] `ls` works
- [ ] `cd /tmp` works and prompt updates
- [ ] `exit` quits the shell
- [ ] Up arrow cycles through history
- [ ] `ls | grep py` works (pipes)
- [ ] `ls > output.txt` works (redirect)
- [ ] `cat < input.txt` works (stdin redirect)
- [ ] `ls >> output.txt` works (append redirect)
- [ ] `echo hello ; echo world` works (semicolons)
- [ ] `export FOO=bar && echo $FOO` works (env vars)

## Key concepts by file

| File | Concepts |
|------|----------|
| lexer.py | Tokenization, shlex, string parsing |
| parser.py | Grammar, AST, dataclasses |
| executor.py | fork/exec, pipes, file descriptors, subprocess |
| builtins.py | Why some commands must be builtins |
| env.py | Process environment, inheritance |
| history.py | readline, file persistence, atexit |

## Ideas for extending once the basics work

- Tab completion (readline completer API)
- `&&` and `||` operators (run next command based on exit code)
- `$?` variable (exit code of last command)
- Glob expansion (`ls *.py`)
- Subshell execution (`$(command)`)
- Job control (`&` for background, `fg`, `bg`, `jobs`)
- A config file (`~/.pyshrc`)
- Custom prompt with git branch, colors
- Alias support
