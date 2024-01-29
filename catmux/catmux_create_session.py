#!/usr/bin/env python
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

import os
import logging
import subprocess
import sys

import argparse

from importlib import resources

import libtmux

from catmux.session import Session as CatmuxSession
import catmux.exceptions


def safe_call(cmd_list):
    """Makes a subprocess check_call and outputs a clear error message on failure and then exits"""
    try:
        subprocess.check_output(cmd_list)
        return True
    except subprocess.CalledProcessError as err_thrown:
        print('Error while calling "%s"', err_thrown.cmd)
        return False


def parse_arguments(debug=False):
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Create a new catmux session")
    parser.add_argument(
        "session_config", help="Session configuration. Should be a yaml-file."
    )
    parser.add_argument(
        "-n", "--session_name", default="catmux", help="Name used for the tmux session"
    )
    parser.add_argument(
        "-L", "--server-name", default="catmux", help="tmux server to use"
    )
    parser.add_argument(
        "-t", "--tmux_config", help="This config will be used for the tmux session"
    )
    parser.add_argument(
        "-d", "--detach", action="store_true", help="Start session in detached mode"
    )
    parser.add_argument(
        "--overwrite",
        help="Overwrite a parameter from the session config. Parameters can be "
        "specified using a comma-separated list such as '--overwrite "
        "param_a=1,param_b=2'.",
    )

    args = parser.parse_args()
    if debug:
        print(args)
    return args


def main():
    """Creates a new tmux session if it does not yet exist"""
    args = parse_arguments()

    if args.tmux_config:
        tmux_config = args.tmux_config
        if not os.path.exists(tmux_config):
            print("Given tmux_config file does not exist")
            sys.exit(1)
    elif os.path.exists(os.path.expanduser("~/.tmux.conf")):
        tmux_config = os.path.expanduser("~/.tmux.conf")
    elif os.path.exists("/etc/tmux.conf"):
        tmux_config = "/etc/tmux.conf"
    else:
        with resources.path(
            ".".join(["catmux", "resources"]), "tmux_default.conf"
        ) as catmux_session:
            tmux_config = str(catmux_session)
    print("Using tmux config file: {}".format(tmux_config))

    tmux_server = libtmux.Server(args.server_name, config_file=tmux_config)
    try:
        tmux_server.sessions.get(session_name=args.session_name)
        print(
            f'Session with name "{args.session_name}" already exists. Not overwriting session.'
        )
        sys.exit(1)
    except libtmux.exc.ObjectDoesNotExist:
        # If no session with that name can be found, everything is fine...
        pass

    session_config = CatmuxSession(
        session_name=args.session_name,
        runtime_params=args.overwrite,
    )
    try:
        session_config.init_from_filepath(args.session_config)
        print(f'Created session "{args.session_name}"')

        target_session = session_config.run(tmux_server)
        if not args.detach:
            tmux_server.attach_session(target_session=args.session_name)
    except Exception as err:
        logging.error(err)
        tmux_server.kill_session(args.session_name)
        sys.exit(1)
