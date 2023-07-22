import os

from catmux.session import check_boolean_field
from catmux.tmux_wrapper import _safe_call as safe_call
from catmux.prefix import get_prefix
import catmux.resources


def test_boolean_field():
    assert check_boolean_field("yes") == True
    assert check_boolean_field("Yes") == True
    assert check_boolean_field("YES") == True
    assert check_boolean_field("true") == True
    assert check_boolean_field("True") == True
    assert check_boolean_field("TRUE") == True
    assert check_boolean_field("t") == True
    assert check_boolean_field("T") == True
    assert check_boolean_field("1") == True
    assert check_boolean_field("no") == False
    assert check_boolean_field("No") == False
    assert check_boolean_field("NO") == False
    assert check_boolean_field("false") == False
    assert check_boolean_field("False") == False
    assert check_boolean_field("FALSE") == False
    assert check_boolean_field(True) == True
    assert check_boolean_field(False) == False


def test_safe_call():
    assert safe_call(["bash", "-c", "exit 0"]) == True
    assert safe_call(["bash", "-c", "exit 1"]) == False
    assert safe_call(["bash", "-c", "return 0"]) == False  #  illegal bash


def test_get_prefix():
    prefix = os.path.join(get_prefix(), "__init__.py")
    assert prefix == catmux.resources.__file__
