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

import libtmux

from catmux.split import Split
from catmux.exceptions import InvalidConfig


class Window(object):

    """Class to represent a tmux window structure"""

    def __init__(self, **kwargs):
        """TODO: to be defined1."""

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

    def run(self, parent_session: libtmux.Session, first=False):
        """Creates the window"""
        window_name = getattr(self, "name")
        target_window = None
        if not first:
            target_window = parent_session.new_window(window_name)
        else:
            target_window = parent_session.windows[0]
            target_window.rename_window(window_name)

        for counter, split in enumerate(self.splits):
            if counter > 0:
                target_window.split_window()
            target_pane = target_window.panes[-1]

            if hasattr(self, "before_commands"):
                for cmd in getattr(self, "before_commands"):
                    target_pane.send_keys(cmd)

            split.run(target_pane)
        if hasattr(self, "layout"):
            target_window.select_layout(getattr(self, "layout"))

        if hasattr(self, "delay"):
            print(
                "Window {} requested delay of {} seconds".format(
                    getattr(self, "name"), getattr(self, "delay")
                )
            )
            time.sleep(getattr(self, "delay"))
