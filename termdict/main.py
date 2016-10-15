#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys
from MWDict import MWDict  


def remove_dups(arg_list):
    
    no_dups = []
    for arg in arg_list:
        if arg not in no_dups:
            no_dups.append(arg)
    
    return no_dups


def main(args):
    
    dicts = []
    args = remove_dups(args)
    for arg in args:
        if arg.lower() == "mw":
            dicts.append(MWDict())
        else:
            print "No such dictionary."
            print "Dictionary(s) available: MW(Merriam-Webster)."
            print "Please try again"
            sys.exit()
    
    while True:
        try:
            word = raw_input()
            [d.translate(word.strip()) for d in dicts]
        except KeyboardInterrupt:
            [d.close() for d in dicts]
            print "Program Exit"
            sys.exit()
                  
if __name__ == "__main__":
    
    main(sys.argv[1:])    
    
