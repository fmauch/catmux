# -- BEGIN LICENSE BLOCK ----------------------------------------------

# catmux
# Copyright (C) 2018  Felix Mauch
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -- END LICENSE BLOCK ------------------------------------------------

"""A split in a tmux session"""

import catmux.tmux_wrapper as tmux


class Split(object):

    """A split is a pane where commands can be executed"""

    def __init__(self, **kwargs):
        """TODO: to be defined1."""

        if kwargs is not None:
            for (key, value) in kwargs.items():
                setattr(self, key, value)

    def debug(self, name="", prefix=""):
        """Prints all information about this window"""
        print(prefix + "- Split " + name + ":")
        if hasattr(self, "commands"):
            print(prefix + "  commands: ")
            print("\t- " + "\n\t- ".join(getattr(self, "commands")))

    def run(self, server_name, target_window=None):
        "Executes all configured commands" ""
        tmux_wrapper = tmux.TmuxWrapper(server_name=server_name)
        for command in getattr(self, "commands"):
            tmux_wrapper.send_keys(command, target_window)
