#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

HOME = os.path.expanduser("~")
DIR = os.path.join(HOME, ".termdict")
ROWS, COLUMNS = map(lambda x: int(x), os.popen('stty size', 'r').read().split())

