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

"""Contains the Window object"""
from __future__ import print_function

import tmux_wrapper as tmux


class Window(object):

    """Class to represent a tmux window structure"""

    def __init__(self, name, **kwargs):
        """TODO: to be defined1. """

        self._name = name
        self.before_commands = list()
        self.commands = list()

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                setattr(self, key, value)


    def debug(self):
        """Prints all information about this window"""
        print('\n----- {} -----'.format(self._name))
        if hasattr(self, 'before_commands'):
            print('before_commands: ')
            print('\n\t- '.join(getattr(self, 'before_commands')))
        if hasattr(self, 'before_commands'):
            print('commands: ')
            print('\n\t- '.join(getattr(self, 'commands')))

    def create(self):
        """Creates the window"""
        tmux.tmux_call(['new-window'])
        tmux.tmux_call(['rename-window', self._name])
        for command in getattr(self, 'before_commands'):
            tmux.send_keys(command)

    def run(self):
        "Executes all configured commands"""
        for cmd in getattr(self, 'commands'):
            tmux.send_keys(cmd)

