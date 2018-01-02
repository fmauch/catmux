# -- BEGIN LICENSE BLOCK ----------------------------------------------

# catmux
# Copyright (C) 2018  Felix Mauch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -- END LICENSE BLOCK ------------------------------------------------

"""Contains everything around the config file"""
from __future__ import print_function


import yaml
from window import Window


class Session(object):

    """Parser for a config yaml file"""

    def __init__(self):
        """TODO: to be defined1. """

        self._common = dict()
        self._windows = list()
        self.__yaml_data = None

    def init_from_filepath(self, filepath):
        """Initializes the data from a file read from filepath."""

        try:
            self.__yaml_data = yaml.load(file(filepath, 'r'))
        except yaml.YAMLError as exc:
            print('Error while loading config file: %s', exc)
            print('Loaded file was: %s', filepath)

        self.init_from_yaml(self.__yaml_data)

    def init_from_yaml(self, yaml_data):
        """Initialize config directly by an already loaded yaml structure."""

        self.__yaml_data = yaml_data

        self._parse_common()
        self._parse_windows()

    def run(self):
        """Runs the loaded session"""
        if len(self._windows) == 0:
            print('No windows to run found')
            return

        for window in self._windows:
            window.debug()
            window.create()
            window.run()

    def _parse_common(self):
        if self.__yaml_data is None:
            print('parse_common was called without yaml data loaded.')
            raise RuntimeError

        if 'common' in self.__yaml_data:
            self._common = self.__yaml_data['common']

    def _parse_windows(self):
        if self.__yaml_data is None:
            print('parse_windows was called without yaml data loaded.')
            raise RuntimeError

        if 'windows' in self.__yaml_data:
            for window in self.__yaml_data['windows']:
                commands = list()
                before_commands = list()
                if 'before_commands' in self._common:
                    before_commands = self._common['before_commands']

                if 'commands' in window:
                    commands = window['commands']
                if 'before_commands' in window:
                    before_commands = window['before_commands']
                self._windows.append(
                    Window(
                        window['name'],
                        commands=commands,
                        before_commands=before_commands))
        else:
            print('No window section found in session config')
