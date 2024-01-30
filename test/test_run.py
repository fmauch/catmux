import unittest

import libtmux
import yaml

from catmux.split import Split as Split
from catmux.session import Session


class CustomAssertions:
    def assertFileExists(self, path):
        if not os.path.lexists(path):
            raise AssertionError('File not exists in path "' + path + '".')

    def assert_cmd_in_output(self, cmd: str, output: list):
        merged_output = "\n".join(output)
        if not any(cmd in x for x in output):
            raise AssertionError(
                f"{cmd} is not in output. Output was \n{merged_output}"
            )


class CatmuxFullTest(unittest.TestCase, CustomAssertions):
    def setUp(self):
        self.server_name = "catmux_test"
        self.tmux_server = libtmux.Server(socket_name=self.server_name)

    def tearDown(self):
        self.tmux_server.kill_server()

    def test_full_circle(self):
        CONFIG = """common:
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
        session_name = "foo"
        session = Session(session_name=session_name)
        session.init_from_yaml(yaml.safe_load(CONFIG))

        session.run(parent_server=self.tmux_server, debug=True)

        # This would throw an ObjectNotFound error when the session doesn't exist
        tmux_session = self.tmux_server.sessions.get(session_name=session_name)
        win_foobar = tmux_session.windows.get(window_name="foobar")
        foobar_out = win_foobar.panes[0].capture_pane(start=-10)
        win_hello = tmux_session.windows.get(window_name="hello")
        hello_out_0 = win_hello.panes[0].capture_pane(start=-10)
        hello_out_1 = win_hello.panes[1].capture_pane(start=-10)

        self.assertEqual(len(win_foobar.panes), 1)
        self.assert_cmd_in_output('echo "hello"', foobar_out)
        self.assert_cmd_in_output('echo "world"', foobar_out)
        self.assert_cmd_in_output('echo "schubidoo"', foobar_out)

        self.assertEqual(len(win_hello.panes), 2)
        self.assert_cmd_in_output('echo "hello"', hello_out_0)
        self.assert_cmd_in_output('echo "world"', hello_out_0)
        self.assert_cmd_in_output('echo "first_split"', hello_out_0)

        self.assert_cmd_in_output('echo "hello"', hello_out_1)
        self.assert_cmd_in_output('echo "world"', hello_out_1)
        self.assert_cmd_in_output('echo "second_split"', hello_out_1)
