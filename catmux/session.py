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

"""Contains everything around the config file"""
import re
import yaml

from catmux.window import Window
import catmux.tmux_wrapper as tmux
import catmux.exceptions as cme


def check_boolean_field(boolean):
    if isinstance(boolean, bool):
        return boolean
    return boolean.lower() in ("yes", "true", "t", "1", True)


class Session(object):

    """Parser for a config yaml file"""

    def __init__(self, server_name, session_name, runtime_params=None):
        """TODO: to be defined1."""

        self._server_name = server_name
        self._session_name = session_name
        self._parameters = dict()
        self._runtime_params = self._parse_overwrites(runtime_params)
        self._windows = list()
        self.__yaml_data = None

        self._before_commands = list()
        self._default_window = None

    def init_from_filepath(self, filepath):
        """Initializes the data from a file read from filepath."""

        try:
            self.__yaml_data = yaml.safe_load(open(filepath, "r"))
        except yaml.YAMLError as exc:
            raise cme.InvalidConfig(
                f"Config file {filepath} is not a valid yaml file:\n{exc}"
            )

        self.init_from_yaml(self.__yaml_data)

    def init_from_yaml(self, yaml_data):
        """Initialize config directly by an already loaded yaml structure."""

        self.__yaml_data = yaml_data
        self._parse_common()
        self._parse_parameters()
        self._parse_windows()

    def run(self, debug=False):
        """Runs the loaded session"""
        assert len(self._windows) > 0

        first = True
        for window in self._windows:
            window.create(first)
            if debug:
                window.debug()
            first = False

        tmux_wrapper = tmux.TmuxWrapper(self._server_name)
        if self._default_window:
            tmux_wrapper.tmux_call(
                [
                    "select-window",
                    "-t",
                    self._session_name + ":" + self._default_window,
                ]
            )

    def _parse_common(self):
        if self.__yaml_data is None:
            print("parse_common was called without yaml data loaded.")
            raise RuntimeError

        if "common" in self.__yaml_data and self.__yaml_data["common"]:
            common = self.__yaml_data["common"]
            if "before_commands" in common and common["before_commands"]:
                self._before_commands = common["before_commands"]

            if "default_window" in common and common["default_window"]:
                self._default_window = common["default_window"]

    def _parse_overwrites(self, data_string):
        """Separates a comma-separated list of foo=val1,bar=val2 into a dictionary."""
        if data_string is None:
            return None

        overwrites = dict()
        param_list = data_string.split(",")
        for param in param_list:
            key, value = param.split("=")
            overwrites[key] = value

        return overwrites

    def _parse_parameters(self):
        if self.__yaml_data is None:
            print("parse_parameters was called without yaml data loaded.")
            raise RuntimeError
        if "parameters" in self.__yaml_data:
            self._parameters = self.__yaml_data["parameters"]

        print("Parameters found in session config:")
        print(
            " - "
            + "\n - ".join(
                "{} = {}".format(key, value)
                for key, value in list(self._parameters.items())
            )
        )
        if self._runtime_params:
            print("Parameters found during runtime (overwrites):")
            print(
                " - "
                + "\n - ".join(
                    "{} = {}".format(key, value)
                    for key, value in list(self._runtime_params.items())
                )
            )
            # Overwrite parameters given from command line
            self._parameters.update(self._runtime_params)

        self._replace_parameters(self.__yaml_data)

    def _replace_parameters(self, data):
        if isinstance(data, dict):
            for key, value in list(data.items()):
                data[key] = self._replace_parameters(value)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                data[index] = self._replace_parameters(item)
        elif isinstance(data, str):
            for key, value in list(self._parameters.items()):
                # print('-\nValue {}: {}\n='.format(value, type(data)))
                # if isinstance(value, str):
                # print('replacing {} in {}'.format(key, data))
                data = re.sub(r"\${%s}" % (key), str(value), data)
        return data

    def _parse_windows(self):
        if self.__yaml_data is None:
            print("parse_windows was called without yaml data loaded.")
            raise RuntimeError

        if "windows" in self.__yaml_data:
            if self.__yaml_data["windows"] is None:
                raise cme.InvalidConfig("The 'windows' block must not be empty.")
            for window in self.__yaml_data["windows"]:
                if "if" in window:
                    print("Detected if condition for window " + window["name"])
                    if window["if"] not in self._parameters:
                        print(
                            "Skipping window "
                            + window["name"]
                            + " because parameter "
                            + window["if"]
                            + " was not found."
                        )
                        continue
                    elif not check_boolean_field(self._parameters[window["if"]]):
                        print(
                            "Skipping window "
                            + window["name"]
                            + " because parameter "
                            + window["if"]
                            + " is switched off globally"
                        )
                        continue
                    else:
                        print(
                            "condition fulfilled: {} == {}".format(
                                window["if"], self._parameters[window["if"]]
                            )
                        )
                if "unless" in window:
                    print("Detected unless condition for window " + window["name"])

                    if window["unless"] in self._parameters:
                        if check_boolean_field(self._parameters[window["unless"]]):
                            print(
                                "Skipping window "
                                + window["name"]
                                + " because parameter "
                                + window["unless"]
                                + " is switched on globally"
                            )
                            continue
                        else:
                            print(
                                "condition fulfilled: {} == {}".format(
                                    window["unless"], self._parameters[window["unless"]]
                                )
                            )

                kwargs = dict()
                kwargs["before_commands"] = [cmd for cmd in self._before_commands]

                kwargs.update(window)

                print(kwargs)

                self._windows.append(
                    Window(self._server_name, self._session_name, **kwargs)
                )
        else:
            raise cme.InvalidConfig("No window section found in session config")
