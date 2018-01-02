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

