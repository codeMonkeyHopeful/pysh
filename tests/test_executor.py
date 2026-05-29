"""
tests/test_executor.py - Tests for executor.py

Run with: pytest tests/test_executor.py -v

Note: these tests actually spawn real processes, so they require
a Unix-like environment (Linux/macOS/WSL). They won't work on
native Windows.
"""

import os
import pytest
from env import Env
from executor import Executor
from parser import Pipeline, Command


@pytest.fixture
def env():
    return Env()


@pytest.fixture
def executor(env):
    return Executor(env)


def make_pipeline(*commands):
    """Helper: build a Pipeline from Command objects."""
    return Pipeline(commands=list(commands))


def make_command(name, args=None, redirect_in=None,
                 redirect_out=None, redirect_append=None):
    """Helper: build a Command."""
    return Command(
        name=name,
        args=args or [],
        redirect_in=redirect_in,
        redirect_out=redirect_out,
        redirect_append=redirect_append,
    )


class TestSingleCommand:
    def test_true_returns_zero(self, executor):
        """`true` command always exits 0."""
        pipeline = make_pipeline(make_command("true"))
        assert executor.execute(pipeline) == 0

    def test_false_returns_nonzero(self, executor):
        """`false` command always exits 1."""
        pipeline = make_pipeline(make_command("false"))
        assert executor.execute(pipeline) != 0

    def test_echo_exits_zero(self, executor):
        pipeline = make_pipeline(make_command("echo", ["hello"]))
        assert executor.execute(pipeline) == 0

    def test_nonexistent_command_returns_nonzero(self, executor):
        """Running a command that doesn't exist should return nonzero."""
        pipeline = make_pipeline(make_command("this_command_does_not_exist_xyz"))
        result = executor.execute(pipeline)
        assert result != 0

    def test_nonexistent_command_does_not_crash(self, executor):
        """Running a missing command should not raise an exception."""
        pipeline = make_pipeline(make_command("this_command_does_not_exist_xyz"))
        executor.execute(pipeline)  # should not raise

    def test_empty_pipeline_returns_zero(self, executor):
        assert executor.execute(Pipeline()) == 0


class TestRedirects:
    def test_redirect_out_creates_file(self, executor, tmp_path):
        outfile = str(tmp_path / "output.txt")
        pipeline = make_pipeline(
            make_command("echo", ["hello"], redirect_out=outfile)
        )
        executor.execute(pipeline)
        assert os.path.exists(outfile)
        assert open(outfile).read().strip() == "hello"

    def test_redirect_out_overwrites_file(self, executor, tmp_path):
        outfile = str(tmp_path / "output.txt")
        # write something first
        open(outfile, "w").write("old content\n")
        pipeline = make_pipeline(
            make_command("echo", ["new"], redirect_out=outfile)
        )
        executor.execute(pipeline)
        assert open(outfile).read().strip() == "new"

    def test_redirect_append(self, executor, tmp_path):
        outfile = str(tmp_path / "output.txt")
        open(outfile, "w").write("line1\n")
        pipeline = make_pipeline(
            make_command("echo", ["line2"], redirect_append=outfile)
        )
        executor.execute(pipeline)
        content = open(outfile).read()
        assert "line1" in content
        assert "line2" in content

    def test_redirect_in(self, executor, tmp_path):
        infile = str(tmp_path / "input.txt")
        outfile = str(tmp_path / "output.txt")
        open(infile, "w").write("hello from file\n")
        pipeline = make_pipeline(
            make_command("cat", redirect_in=infile, redirect_out=outfile)
        )
        executor.execute(pipeline)
        assert open(outfile).read().strip() == "hello from file"


class TestPipeline:
    def test_simple_pipe(self, executor, tmp_path):
        """echo hello | cat should produce 'hello'."""
        outfile = str(tmp_path / "output.txt")
        pipeline = make_pipeline(
            make_command("echo", ["hello"]),
            make_command("cat", redirect_out=outfile),
        )
        executor.execute(pipeline)
        assert open(outfile).read().strip() == "hello"

    def test_pipe_exit_code(self, executor):
        """Exit code should come from the last command in the pipeline."""
        pipeline = make_pipeline(
            make_command("echo", ["hello"]),
            make_command("true"),
        )
        assert executor.execute(pipeline) == 0

    def test_three_command_pipeline(self, executor, tmp_path):
        """echo hello world | cat | cat should still produce 'hello world'."""
        outfile = str(tmp_path / "output.txt")
        pipeline = make_pipeline(
            make_command("echo", ["hello", "world"]),
            make_command("cat"),
            make_command("cat", redirect_out=outfile),
        )
        executor.execute(pipeline)
        assert open(outfile).read().strip() == "hello world"
