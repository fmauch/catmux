"""This module provides the installed prefix of the catmux resources"""
# -- BEGIN LICENSE BLOCK ----------------------------------------------

# catmux
# Copyright (C) 2023  Felix Exner
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
import sys
from importlib import resources


def get_prefix():
    """Returns the path of catmux's resource folder"""

    if sys.version_info.major == 3 and sys.version_info.minor == 9:
        with resources.files("catmux") as path:
            return os.path.join(path, "resources")

    with resources.path("catmux", "resources") as path:
        return path


if __name__ == "__main__":
    print(get_prefix())
