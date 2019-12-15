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
from __future__ import print_function, absolute_import

from future.utils import iteritems

import time

import catmux.tmux_wrapper as tmux
from catmux.split import Split


class Window(object):

    """Class to represent a tmux window structure"""

    def __init__(self, **kwargs):
        """TODO: to be defined1. """

        split_list = kwargs.pop('splits', None)
        if not split_list and 'commands' in kwargs:
            split_dict = dict()
            split_dict['commands'] = kwargs.pop('commands')
            split_list = [split_dict]

        self.splits = list()
        for split_data in split_list:
            self.splits.append(Split(**split_data))

        if kwargs is not None:
            for (key, value) in iteritems (kwargs):
                setattr(self, key, value)


    def debug(self):
        """Prints all information about this window"""
        print('\n----- {} -----'.format(getattr(self, 'name')))
        if hasattr(self, 'before_commands'):
            print('before_commands: ')
            print('\t- ' + '\n\t- '.join(getattr(self, 'before_commands')))
        print('Splits:')
        for counter, split in enumerate(self.splits):
            split.debug(name=str(counter), prefix=' ')

    def create(self, session_name, first=False):
        """Creates the window"""
        if not first:
            tmux.tmux_call(['new-window'])
        tmux.tmux_call(['rename-window', getattr(self, 'name')])
        for counter, split in enumerate(self.splits):
            if counter > 0:
                tmux.split()

            if hasattr(self, 'before_commands'):
                for cmd in getattr(self, 'before_commands'):
                    tmux.send_keys(cmd)
            split.run()

        if hasattr(self, 'layout'):
            tmux.tmux_call(['select-layout', getattr(self, 'layout')])

        if hasattr(self, 'delay'):
            print('Window {} requested delay of {} seconds'
                    .format(getattr(self, 'name'), getattr(self, 'delay')))
            time.sleep(getattr(self, 'delay'))
