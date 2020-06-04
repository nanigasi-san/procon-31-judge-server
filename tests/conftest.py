import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../src/"))
from judge.field import Field
@pytest.fixture
def field() -> Field:
    return Field((12, 12))
