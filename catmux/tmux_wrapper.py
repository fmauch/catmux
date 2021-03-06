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

"""Wraps usage of tmux commands"""
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
