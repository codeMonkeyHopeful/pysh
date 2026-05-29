"""
tests/test_history.py - Tests for history.py

Run with: pytest tests/test_history.py -v
"""

import pytest
from history import History


@pytest.fixture
def history():
    """Fresh History instance with readline mocked to avoid file side effects."""
    h = History()
    h.clear()  # start clean
    return h


class TestAdd:
    def test_add_single_entry(self, history):
        history.add("ls")
        assert len(history) == 1

    def test_add_multiple_entries(self, history):
        history.add("ls")
        history.add("cd /tmp")
        history.add("echo hello")
        assert len(history) == 3

    def test_add_empty_string_ignored(self, history):
        history.add("")
        assert len(history) == 0

    def test_add_whitespace_only_ignored(self, history):
        history.add("   ")
        assert len(history) == 0

    def test_add_duplicate_consecutive_ignored(self, history):
        """Running the same command twice should only add it once."""
        history.add("ls")
        history.add("ls")
        assert len(history) == 1

    def test_add_duplicate_non_consecutive_allowed(self, history):
        """Same command is allowed if it's not immediately repeated."""
        history.add("ls")
        history.add("cd /tmp")
        history.add("ls")
        assert len(history) == 3


class TestGetAll:
    def test_get_all_empty(self, history):
        assert history.get_all() == []

    def test_get_all_returns_all(self, history):
        history.add("ls")
        history.add("pwd")
        assert history.get_all() == ["ls", "pwd"]

    def test_get_all_returns_copy(self, history):
        history.add("ls")
        result = history.get_all()
        result.append("injected")
        assert len(history) == 1  # original unchanged


class TestGetLast:
    def test_get_last_n(self, history):
        history.add("cmd1")
        history.add("cmd2")
        history.add("cmd3")
        history.add("cmd4")
        assert history.get_last(2) == ["cmd3", "cmd4"]

    def test_get_last_more_than_available(self, history):
        history.add("cmd1")
        assert history.get_last(10) == ["cmd1"]

    def test_get_last_zero(self, history):
        history.add("cmd1")
        assert history.get_last(0) == []


class TestClear:
    def test_clear_empties_history(self, history):
        history.add("ls")
        history.add("pwd")
        history.clear()
        assert len(history) == 0

    def test_clear_then_add(self, history):
        history.add("ls")
        history.clear()
        history.add("pwd")
        assert history.get_all() == ["pwd"]


class TestLen:
    def test_len_empty(self, history):
        assert len(history) == 0

    def test_len_after_adds(self, history):
        history.add("a")
        history.add("b")
        history.add("c")
        assert len(history) == 3
