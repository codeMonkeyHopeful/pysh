"""
tests/conftest.py - Shared pytest configuration and fixtures

Fixtures defined here are available to all test files automatically
without needing to import them.
"""

import sys
import os

# Make sure the project root is on the path so tests can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
