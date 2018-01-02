"""Wraps usage of tmux commands"""
from __future__ import print_function

import subprocess

def send_keys(command):
    """Executes a command in the current tmux pane"""

    tmux_call(['send-keys', command, 'C-m'])

def tmux_call(command_list):
    """Executes a tmux command """
    tmux_cmd = ['tmux'] + command_list

    print(' '.join(tmux_cmd))
    _safe_call(tmux_cmd)

def _safe_call(cmd_list):
    """Makes a subprocess check_call and outputs a clear error message on failure and then exits"""
    try:
        subprocess.check_output(cmd_list)
        return True
    except subprocess.CalledProcessError as err_thrown:
        print('Error while calling "%s"', err_thrown.cmd)
        return False
