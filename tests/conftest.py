"""
Test configuration and shared fixtures for all tests.
"""
import os
import sys
import pytest
from pathlib import Path

# Add the project root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Common fixtures can be added here
