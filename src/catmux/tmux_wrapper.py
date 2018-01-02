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

"""Wraps usage of tmux commands"""
from __future__ import print_function

import subprocess

def send_keys(command):
    """Executes a command in the current tmux pane"""

    tmux_call(['send-keys', command, 'C-m'])

def split():
    """Splits the current pane into two"""
    tmux_call(['split-window'])

def tmux_call(command_list):
    """Executes a tmux command """
    tmux_cmd = ['tmux'] + command_list

    # print(' '.join(tmux_cmd))
    _safe_call(tmux_cmd)

def _safe_call(cmd_list):
    """Makes a subprocess check_call and outputs a clear error message on failure and then exits"""
    try:
        subprocess.check_output(cmd_list)
        return True
    except subprocess.CalledProcessError as err_thrown:
        print('Error while calling "%s"', err_thrown.cmd)
        return False
