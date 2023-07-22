import subprocess
from unittest import mock

import yaml

import catmux.tmux_wrapper as tmw
from catmux.split import Split as Split
from catmux.session import Session


@mock.patch("subprocess.check_output")
def test_tmux_wrapper(mock_popen):
    server_name = "my_server"
    wrapper = tmw.TmuxWrapper(server_name)

    send_keys = "b"
    wrapper.send_keys(send_keys)
    mock_popen.assert_called_once_with(
        ["tmux", "-L", server_name, "send-keys", send_keys, "C-m"]
    )
    mock_popen.reset_mock()

    wrapper.send_keys(send_keys, target_window="foobar")
    mock_popen.assert_called_once_with(
        ["tmux", "-L", server_name, "send-keys", "-t", "foobar", send_keys, "C-m"]
    )
    mock_popen.reset_mock()

    wrapper.split(target_window="foobar")
    mock_popen.assert_called_once_with(
        ["tmux", "-L", server_name, "split-window", "-t", "foobar"]
    )
    mock_popen.reset_mock()


@mock.patch("subprocess.check_output")
def test_run_split(mock_popen):
    server_name = "my_server"

    split_data = {"commands": ["echo 'hello'", "echo 'world'"]}
    split = Split(**split_data)
    split.run(server_name)

    for cmd in split_data["commands"]:
        mock_popen.assert_any_call(["tmux", "-L", server_name, "send-keys", cmd, "C-m"])


@mock.patch("subprocess.check_output")
def test_full_circle(mock_popen):
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
      layout: tiled
      delay: 1
      splits:
        - commands:
          - echo "first_split"
        - commands:
          - echo "second_split"
"""
    server_name = "my_server"
    session_name = "my_session"
    session = Session(server_name=server_name, session_name=session_name)
    session.init_from_yaml(yaml.safe_load(CONFIG))

    session.run(debug=True)
    calls = [
        ["rename-window", "-t", "my_session:$", "foo"],
        ["send-keys", "-t", "my_session:foo", 'echo "hello"', "C-m"],
        ["send-keys", "-t", "my_session:foo", 'echo "world"', "C-m"],
        ["send-keys", "-t", "my_session:foo", 'echo "schubidoo"', "C-m"],
        ["select-window", "-t", "my_session:foobar"],
        ["new-window", "-t", "my_session"],
        ["rename-window", "-t", "my_session:$", "bar"],
        ["send-keys", "-t", "my_session:bar", 'echo "first_split"', "C-m"],
        ["split-window", "-t", "my_session:bar"],
        ["send-keys", "-t", "my_session:bar", 'echo "second_split"', "C-m"],
        ["select-layout", "-t", "my_session:bar", "tiled"],
    ]
    for call in calls:
        mock_popen.assert_any_call(["tmux", "-L", server_name] + call)
