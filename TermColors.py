#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TermColors:

    color_dict = {
                  "purple": '\033[95m',
                  "blue": '\033[94m',
                  "green": '\033[92m',
                  "yellow": '\033[93m',
                  "red": '\033[91m',
                  "END": '\033[0m',
                  "bold": '\033[1m',
                  "underline": '\033[4m',
                 }
            
    def colorize(self, text, *styles):
        
        style_comb = ""
        for style in styles:
            style_comb += self.color_dict[style]
        return style_comb + text + self.color_dict["END"]

