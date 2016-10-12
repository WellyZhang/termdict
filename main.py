#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from models import MWDict  


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
        if arg.lower() == "MW":
            dicts.append(MWDict())
        else:
            print "No such dictionary."
            print "Dictionary(s) available: MW(Merriam-Webster)."
            print "Please try again"
            exit()
    
    while True:
        try:
            word = raw_input()
            tl = [d.translate(word.strip()) for d in dicts]
            [d.pprint(tl) for d in dicts]              
        except KeyboardInterrupt:
            print "Program Exit"
            exit()
                  
if __name__ == "__main__":
    
    main(sys.argv[1:])    
    
