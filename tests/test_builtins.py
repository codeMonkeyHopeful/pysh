"""
tests/test_builtins.py - Tests for builtins.py

Run with: pytest tests/test_builtins.py -v
"""

import os
import pytest
from unittest.mock import patch
from env import Env
from history import History
from builtins import Builtins


@pytest.fixture
def env():
    return Env()


@pytest.fixture
def history():
    return History()


@pytest.fixture
def builtins(env, history):
    return Builtins(env, history)


class TestIsBuiltin:
    def test_cd_is_builtin(self, builtins):
        assert builtins.is_builtin("cd") is True

    def test_exit_is_builtin(self, builtins):
        assert builtins.is_builtin("exit") is True

    def test_echo_is_builtin(self, builtins):
        assert builtins.is_builtin("echo") is True

    def test_export_is_builtin(self, builtins):
        assert builtins.is_builtin("export") is True

    def test_ls_is_not_builtin(self, builtins):
        assert builtins.is_builtin("ls") is False

    def test_unknown_is_not_builtin(self, builtins):
        assert builtins.is_builtin("totally_fake_command") is False


class TestEcho:
    def test_echo_single_word(self, builtins, capsys):
        builtins.echo(["hello"])
        captured = capsys.readouterr()
        assert captured.out == "hello\n"

    def test_echo_multiple_words(self, builtins, capsys):
        builtins.echo(["hello", "world"])
        captured = capsys.readouterr()
        assert captured.out == "hello world\n"

    def test_echo_empty(self, builtins, capsys):
        builtins.echo([])
        captured = capsys.readouterr()
        assert captured.out == "\n"

    def test_echo_no_newline_flag(self, builtins, capsys):
        builtins.echo(["-n", "hello"])
        captured = capsys.readouterr()
        assert captured.out == "hello"
        assert not captured.out.endswith("\n")

    def test_echo_returns_zero(self, builtins):
        assert builtins.echo(["hello"]) == 0


class TestCd:
    def test_cd_to_valid_path(self, builtins):
        original = os.getcwd()
        builtins.cd(["/tmp"])
        assert os.getcwd() == "/tmp"
        os.chdir(original)  # restore

    def test_cd_no_args_goes_home(self, builtins):
        original = os.getcwd()
        home = os.path.expanduser("~")
        builtins.cd([])
        assert os.getcwd() == home
        os.chdir(original)

    def test_cd_tilde_goes_home(self, builtins):
        original = os.getcwd()
        home = os.path.expanduser("~")
        builtins.cd(["~"])
        assert os.getcwd() == home
        os.chdir(original)

    def test_cd_invalid_path_returns_nonzero(self, builtins):
        result = builtins.cd(["/this/path/does/not/exist/xyz"])
        assert result != 0

    def test_cd_invalid_path_does_not_crash(self, builtins):
        """cd to a bad path should print an error but not raise."""
        builtins.cd(["/this/path/does/not/exist/xyz"])  # should not raise

    def test_cd_returns_zero_on_success(self, builtins):
        original = os.getcwd()
        result = builtins.cd(["/tmp"])
        assert result == 0
        os.chdir(original)

    def test_cd_dash_goes_to_previous(self, builtins, env):
        """cd - should return to the previous directory."""
        original = os.getcwd()
        builtins.cd(["/tmp"])
        builtins.cd(["-"])
        assert os.getcwd() == original
        os.chdir(original)


class TestExport:
    def test_export_sets_variable(self, builtins, env):
        builtins.export(["FOO=bar"])
        assert env.get("FOO") == "bar"

    def test_export_returns_zero(self, builtins):
        assert builtins.export(["FOO=bar"]) == 0

    def test_export_with_equals_in_value(self, builtins, env):
        """Values can contain = signs, only split on first one."""
        builtins.export(["FOO=bar=baz"])
        assert env.get("FOO") == "bar=baz"

    def test_export_no_args_does_not_crash(self, builtins, capsys):
        """export with no args should print variables or do nothing."""
        builtins.export([])  # should not raise


class TestUnset:
    def test_unset_removes_variable(self, builtins, env):
        env.set("TEMP", "value")
        builtins.unset(["TEMP"])
        assert env.get("TEMP") is None

    def test_unset_nonexistent_does_not_crash(self, builtins):
        builtins.unset(["DOES_NOT_EXIST"])  # should not raise

    def test_unset_returns_zero(self, builtins):
        assert builtins.unset(["ANYTHING"]) == 0


class TestHelp:
    def test_help_prints_output(self, builtins, capsys):
        builtins.help([])
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_help_shows_cd(self, builtins, capsys):
        builtins.help([])
        captured = capsys.readouterr()
        assert "cd" in captured.out

    def test_help_returns_zero(self, builtins):
        assert builtins.help([]) == 0
