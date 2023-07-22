import os
import sys

import pytest

from importlib import resources
import tempfile
import yaml

from catmux.session import Session
import catmux.exceptions


def test_common_block():
    CONFIG = """common:
    before_commands:
        - echo "hello"
        - echo "world"
    default_window: foobar
windows:
    - name: foo
      commands:
          - echo "bar"
"""

    session = Session("server", "name")
    session.init_from_yaml(yaml.safe_load(CONFIG))

    assert session._before_commands == ['echo "hello"', 'echo "world"']
    assert session._default_window == "foobar"


def test_no_common_block():
    CONFIG = """windows:
    - name: left-right
      splits:
        - commands:
          - echo "left"
    - name: foo
      splits:
        - commands:
          - echo "left"
"""
    session = Session("server", "name")
    session.init_from_yaml(yaml.safe_load(CONFIG))

    assert len(session._before_commands) == 0
    assert session._default_window == None


def test_empty_common_block():
    CONFIG = """common:
windows:
    - name: left-right
      splits:
        - commands:
          - echo "left"
    - name: foo
      splits:
        - commands:
          - echo "left"
"""
    session = Session("server", "name")
    session.init_from_yaml(yaml.safe_load(CONFIG))

    assert len(session._before_commands) == 0
    assert session._default_window == None


def test_empty_before_commands():
    CONFIG = """common:
    before_commands:
windows:
    - name: left-right
      splits:
        - commands:
          - echo "left"
    - name: foo
      splits:
        - commands:
          - echo "left"
"""
    session = Session("server", "name")
    session.init_from_yaml(yaml.safe_load(CONFIG))

    assert len(session._before_commands) == 0
    assert session._default_window == None


def test_missing_parameter_for_if_unless():
    CONFIG = """common:
    before_commands:
        - echo "hello"
        - echo "world"
    default_window: foobar
windows:
    - name: left-right
      if: show_layouts
      splits:
        - commands:
          - echo "left"
    - name: foo
      unless: show_layouts
      splits:
        - commands:
          - echo "left"
"""
    session = Session("server", "name")
    session.init_from_yaml(yaml.safe_load(CONFIG))


def test_parameter_replacement():
    CONFIG = """common:
    before_commands:
        - echo "hello"
        - echo "world"
    default_window: foobar
parameters:
    replacement_param: schubidoo
    show_layouts: true

windows:
    - name: foo
      if: show_layouts
      commands:
        - echo "${replacement_param}"
    - name: bar
      unless: show_layouts
      commands:
        - echo "I will not be printed when layouts are shown"
"""
    session = Session("server", "name")
    session.init_from_yaml(yaml.safe_load(CONFIG))

    assert session._parameters["replacement_param"] == "schubidoo"
    assert getattr(session._windows[0].splits[0], "commands")[0] == 'echo "schubidoo"'


def test_split_without_command():
    CONFIG = """windows:
    - name: foo
      layout: tiled
"""
    session = Session("server", "name")
    with pytest.raises(catmux.exceptions.InvalidConfig):
        session.init_from_yaml(yaml.safe_load(CONFIG))


def test_empty_config():
    CONFIG = """foo: bar
"""
    session = Session("server", "name")
    with pytest.raises(catmux.exceptions.InvalidConfig):
        session.init_from_yaml(yaml.safe_load(CONFIG))


def test_empty_windows_block():
    CONFIG = """windows:
"""
    session = Session("server", "name")
    with pytest.raises(catmux.exceptions.InvalidConfig):
        session.init_from_yaml(yaml.safe_load(CONFIG))


def test_parsing_overwrites():
    CONFIG = """---
common:
  before_commands:
    - echo "This is a catmux window :)"
  default_window: some_other_window
parameters:
  show_layouts: false
  replacement_param: world
windows:
    - name: foo
      commands:
        - echo "bar"
"""
    session = Session("server", "name", runtime_params=None)
    session.init_from_yaml(yaml.safe_load(CONFIG))

    session = Session(
        "server", "name", runtime_params="show_layouts=true, replacement_param=foobar"
    )
    session.init_from_yaml(yaml.safe_load(CONFIG))


def test_init_from_file():
    with resources.path(
        ".".join(["catmux", "resources"]), "example_session.yaml"
    ) as catmux_session:
        session = Session("server", "name")
        session.init_from_filepath(catmux_session)


def test_illegal_file():
    fd, session_config = tempfile.mkstemp()
    CONFIG = """[block name]
this is not a yaml file;
this is something else.
"""
    with os.fdopen(fd, "w") as f:
        f.write(CONFIG)

    session = Session("server", "name")
    with pytest.raises(catmux.exceptions.InvalidConfig):
        session.init_from_filepath(session_config)


def test_parsing_without_yaml():
    session = Session("server", "name")
    with pytest.raises(RuntimeError):
        session._parse_common()
    with pytest.raises(RuntimeError):
        session._parse_parameters()
    with pytest.raises(RuntimeError):
        session._parse_windows()
