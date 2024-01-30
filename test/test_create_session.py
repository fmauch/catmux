import os
import pytest
from tempfile import mkstemp

from importlib import resources
import libtmux
import yaml

import catmux.catmux_create_session

# from catmux.session import Session


@pytest.fixture()
def tmux_server():
    server = libtmux.Server(socket_name="catmux_test_96754")
    yield server
    server.kill_server()


def test_resolve_config_path(fs):
    with pytest.raises(OSError):
        catmux.catmux_create_session.resolve_tmux_config_path(
            "/this/file/does/not/exist/probably"
        )
        with resources.path(
            ".".join(["catmux", "resources"]), "tmux_default.conf"
        ) as catmux_session:
            tmux_config = str(catmux_session)
            assert tmux_config == catmux.catmux_create_session.resolve_tmux_config_path(
                None
            )

    with resources.path(
        ".".join(["catmux", "resources"]), "tmux_default.conf"
    ) as catmux_session:
        tmux_config = str(catmux_session)
        fs.create_file(tmux_config)
        assert tmux_config == catmux.catmux_create_session.resolve_tmux_config_path(
            None
        )
    fs.create_file(os.path.expanduser("/etc/tmux.conf"))
    assert os.path.expanduser(
        "/etc/tmux.conf"
    ) == catmux.catmux_create_session.resolve_tmux_config_path(None)
    fs.create_file(os.path.expanduser("~/.tmux.conf"))
    assert os.path.expanduser(
        "~/.tmux.conf"
    ) == catmux.catmux_create_session.resolve_tmux_config_path(None)


def test_checking_for_existing_session(tmux_server):
    tmux_server.new_session(session_name="foo_session")
    assert (
        catmux.catmux_create_session.check_for_existing_session(
            tmux_server, "bar_session"
        )
        == False
    )
    assert (
        catmux.catmux_create_session.check_for_existing_session(
            tmux_server, "foo_session"
        )
        == True
    )


def test_create_session(tmux_server):
    session_config, file_path = mkstemp()
    session_name = "test_session"
    overwrites = None
    with os.fdopen(session_config, "w") as f:
        f.write(
            """common:
    before_commands:
        - echo "hello"
        - echo "world"
    default_window: foobar
parameters:
    replacement_param: schubidoo
    show_layouts: true

windows:
    - name: foobar
      if: show_layouts
      commands:
        - echo "${replacement_param}"
    - name: hello
      layout: tiled
      delay: 1
      splits:
        - commands:
          - echo "first_split"
        - commands:
          - echo "second_split"
"""
        )
    catmux.catmux_create_session.create_session(
        tmux_server, file_path, session_name, overwrites
    )
