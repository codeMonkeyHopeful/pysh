"""
tests/test_env.py - Tests for env.py

Run with: pytest tests/test_env.py -v
"""

import os
import pytest
from env import Env


@pytest.fixture
def env():
    """Creates a fresh Env instance for each test."""
    return Env()


class TestGet:
    def test_get_existing_key(self, env):
        """Should return the value for a key that exists."""
        env._env["FOO"] = "bar"
        assert env.get("FOO") == "bar"

    def test_get_missing_key_returns_none(self, env):
        """Should return None when key doesn't exist and no default given."""
        assert env.get("DOES_NOT_EXIST") is None

    def test_get_missing_key_returns_default(self, env):
        """Should return the default value when key doesn't exist."""
        assert env.get("DOES_NOT_EXIST", "fallback") == "fallback"

    def test_get_inherited_path(self, env):
        """PATH should exist since we copy os.environ on init."""
        assert env.get("PATH") is not None


class TestSet:
    def test_set_new_variable(self, env):
        """Should store a new variable."""
        env.set("MY_VAR", "hello")
        assert env.get("MY_VAR") == "hello"

    def test_set_updates_os_environ(self, env):
        """Setting a variable should also update os.environ."""
        env.set("MY_VAR", "hello")
        assert os.environ.get("MY_VAR") == "hello"
        # cleanup
        del os.environ["MY_VAR"]

    def test_set_overwrites_existing(self, env):
        """Setting an existing variable should overwrite it."""
        env.set("FOO", "first")
        env.set("FOO", "second")
        assert env.get("FOO") == "second"


class TestUnset:
    def test_unset_removes_variable(self, env):
        """Should remove a variable that exists."""
        env.set("TEMP_VAR", "value")
        env.unset("TEMP_VAR")
        assert env.get("TEMP_VAR") is None

    def test_unset_removes_from_os_environ(self, env):
        """Unsetting should also remove from os.environ."""
        env.set("TEMP_VAR", "value")
        env.unset("TEMP_VAR")
        assert os.environ.get("TEMP_VAR") is None

    def test_unset_nonexistent_does_not_raise(self, env):
        """Unsetting a variable that doesn't exist should not raise."""
        env.unset("DOES_NOT_EXIST")  # should not raise


class TestGetEnv:
    def test_returns_dict(self, env):
        """get_env should return a dict."""
        assert isinstance(env.get_env(), dict)

    def test_returns_copy(self, env):
        """get_env should return a copy, not the internal dict."""
        result = env.get_env()
        result["NEW_KEY"] = "new_value"
        assert env.get("NEW_KEY") is None  # original should be unchanged

    def test_contains_set_variables(self, env):
        """Variables set via set() should appear in get_env()."""
        env.set("FOO", "bar")
        assert env.get_env()["FOO"] == "bar"


class TestPrevDir:
    def test_prev_dir_starts_none(self, env):
        """Previous directory should be None initially."""
        assert env.get_prev_dir() is None

    def test_set_and_get_prev_dir(self, env):
        """Should store and retrieve the previous directory."""
        env.set_prev_dir("/tmp")
        assert env.get_prev_dir() == "/tmp"


class TestExpand:
    def test_expand_no_variables(self, env):
        """String with no variables should be returned unchanged."""
        assert env.expand("hello world") == "hello world"

    def test_expand_known_variable(self, env):
        """Should expand a $VAR that exists in the environment."""
        env.set("GREETING", "hello")
        assert env.expand("$GREETING world") == "hello world"

    def test_expand_unknown_variable(self, env):
        """Unknown $VAR should expand to empty string."""
        result = env.expand("$TOTALLY_UNKNOWN_VAR_XYZ")
        assert result == ""

    def test_expand_multiple_variables(self, env):
        """Should expand multiple variables in one string."""
        env.set("FIRST", "hello")
        env.set("SECOND", "world")
        assert env.expand("$FIRST $SECOND") == "hello world"
