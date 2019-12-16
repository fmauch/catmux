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

"""A split in a tmux session"""
from __future__ import print_function, absolute_import

from future.utils import iteritems

import catmux.tmux_wrapper as tmux


class Split(object):

    """A split is a pane where commands can be executed"""

    def __init__(self, **kwargs):
        """TODO: to be defined1. """

        if kwargs is not None:
            for (key, value) in iteritems(kwargs):
                setattr(self, key, value)

    def debug(self, name='', prefix=''):
        """Prints all information about this window"""
        print(prefix + '- Split ' + name + ':')
        if hasattr(self, 'commands'):
            print(prefix + '  commands: ')
            print('\t- ' + '\n\t- '.join(getattr(self, 'commands')))

    def run(self):
        "Executes all configured commands"""
        for command in getattr(self, 'commands'):
            tmux.send_keys(command)
