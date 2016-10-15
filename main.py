#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import config
from mwdict import MWDict
from termcolors import TermColors

def remove_dups(arg_list):
    
    no_dups = []
    for arg in arg_list:
        if arg not in no_dups:
            no_dups.append(arg)
    
    return no_dups
    

def welcome():
    
    os.system("clear")
    header = "Welcome to TermDict, a Parsing-based Dictionary Framework"
    print tc.colorize(header, "yellow").center(
              config.COLUMNS)
    print tc.colorize("========================", "yellow").center(
              config.COLUMNS)
    print tc.colorize("==   by Welly Zhang   ==", "yellow").center(
              config.COLUMNS)
    print tc.colorize("========================", "yellow").center(
              config.COLUMNS)

def main(args):
    
    welcome()
    dicts = []
    args = remove_dups(args)
    for arg in args:
        if arg.lower() == "mw":
            dicts.append(MWDict())
            print tc.colorize("Loading Merriam-Webster ... Done!", "red")
        else:
            warning = tc.colorize("Warning: ", "bold", "red")
            warning += ("No such dictionary. Dictionary(s) available: "
                       "MW(Merriam-Webster). Please try again.")
            print warning
            sys.exit()
    
    while True:
        try:
            print tc.colorize("\nSearch for:", "blue"), 
            word = raw_input()
            [d.translate(word.strip()) for d in dicts]
        except KeyboardInterrupt:
            [d.close() for d in dicts]
            print tc.colorize("Program Exit", "red", "bold")
            sys.exit()
                  
if __name__ == "__main__":
    
    global tc
    tc = TermColors()
    main(sys.argv[1:])    
    
