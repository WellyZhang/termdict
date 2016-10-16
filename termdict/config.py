#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os


# home directory
HOME = os.path.expanduser("~")

# database directory
DIR = os.path.join(HOME, ".termdict")

# size of the terminal
ROWS, COLUMNS = map(lambda x: int(x), os.popen('stty size', 'r').read().split())

# version number
VERSION = "0.1.2"
