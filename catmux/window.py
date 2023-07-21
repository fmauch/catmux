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

"""Contains the Window object"""
import time

import catmux.tmux_wrapper as tmux
from catmux.split import Split
from catmux.exceptions import InvalidConfig


class Window(object):

    """Class to represent a tmux window structure"""

    def __init__(self, server_name, session_name, **kwargs):
        """TODO: to be defined1."""

        self.server_name = server_name
        self.session_name = session_name

        split_list = kwargs.pop("splits", None)
        if not split_list:
            if "commands" in kwargs:
                split_dict = dict()
                split_dict["commands"] = kwargs.pop("commands")
                split_list = [split_dict]
            else:
                raise InvalidConfig(
                    f"No splits and no commands given for window '{kwargs['name']}'."
                )

        print(split_list)

        self.splits = list()
        for split_data in split_list:
            self.splits.append(Split(**split_data))

        if kwargs is not None:
            for (key, value) in kwargs.items():
                setattr(self, key, value)

    def debug(self):
        """Prints all information about this window"""
        print("\n----- {} -----".format(getattr(self, "name")))
        if hasattr(self, "before_commands"):
            print("before_commands: ")
            print("\t- " + "\n\t- ".join(getattr(self, "before_commands")))
        print("Splits:")
        for counter, split in enumerate(self.splits):
            split.debug(name=str(counter), prefix=" ")

    def create(self, first=False):
        """Creates the window"""
        tmux_wrapper = tmux.TmuxWrapper(server_name=self.server_name)
        target_window = ":".join([self.session_name, getattr(self, "name")])
        if not first:
            tmux_wrapper.tmux_call(["new-window", "-t", self.session_name])
        tmux_wrapper.tmux_call(
            ["rename-window", "-t", f"{self.session_name}:$", getattr(self, "name")]
        )
        for counter, split in enumerate(self.splits):
            if counter > 0:
                tmux_wrapper.split(target_window)

            if hasattr(self, "before_commands"):
                for cmd in getattr(self, "before_commands"):
                    tmux_wrapper.send_keys(cmd, target_window=target_window)
            split.run(server_name=self.server_name, target_window=target_window)

        if hasattr(self, "layout"):
            tmux_wrapper.tmux_call(
                ["select-layout", "-t", target_window, getattr(self, "layout")]
            )

        if hasattr(self, "delay"):
            print(
                "Window {} requested delay of {} seconds".format(
                    getattr(self, "name"), getattr(self, "delay")
                )
            )
            time.sleep(getattr(self, "delay"))
