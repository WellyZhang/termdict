#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
from basedict import BaseDict

class MWDict(BaseDict):
    
    def __init__(self):
    
        BaseDict.__init__(self, 
                          "http://www.merriam-webster.com/dictionary/",
                          "mw")
        
    def parse_web(self, soup):
        
        def has_word_header(inner_box):
            
            if inner_box.find("div", {"class": "word-header"}) is not None:
                return True
            else:
                return False
        
        def mode_checker(inner_box):
            
            msg = inner_box.find("div", {"class": "card-primary-content"})
            has_wd = None
            mode = None
            if (msg is not None and 
                msg.text.strip().startswith("The word you've")):
                    mode = "err_sug"
            elif (msg is not None and 
                msg.text.strip().startswith("Words fail us")):
                    mode = "err_fail"
            else:            
                has_wd = has_word_header(inner_box)
                if has_wd:
                    h2 = inner_box.find("div", {"class": "word-sub-header"})
                    h2 = h2.text.strip()
                else:
                    h2 = inner_box.h2.text.strip()
                    
                if h2.startswith("Definition") or \
                    h2.startswith("Full Definition") or \
                    h2.startswith("Medical Definition"):
                    mode = "def"
                elif h2.startswith("Simple Definition"):
                    mode = "sdef"
                elif h2.startswith("Examples"):
                    mode = "eg"
                        
            return has_wd, mode
        
        def header_handler(content, main=False):
        
            spell = content.find("div", {"class": "word-header"})
            if main:
                spell = spell.h1.text.strip()
            else:
                spell = spell.h2.text.strip()
                
            attrs = content.find("div", {"class": "word-attributes"})
            attrs = " ".join(attrs.text.split())
                        
            return spell, attrs
         
        def content_handler(content, has_wd, mode, ret, main=False):
            
            if mode == "err_sug":
                suggests = content.findAll("a")
                sug_list = []
                for suggest in suggests:
                     sug_list.append(suggest.text.strip())
                ret.append(("suggests", sug_list))
            elif mode == "err_fail":
                ret.append(("fail", "Words fail us. Try again."))
                
            else: 
                if has_wd:
                    header = header_handler(content, main)
                    ret.append(("spelling", header[0]))
                    ret.append(("attrs", header[1]))
                    
                if mode == "def":
                    inflections = content.find("span", {"class": "inflections"})
                    if inflections is not None:
                        children = inflections.children
                        inflections = ""
                        for child in children:
                            text = child.text.split()
                            if "play" in text:
                                text.remove("play")
                            text = " ".join(text)
                            inflections += text + " "
                        ret.append(("inflections", inflections))                
                    
                    content = content.find("div", {"class": 
                                "card-primary-content"})
                                
                    lists = content.findAll("li")
                    
                    def_list = []
                    for l in lists:
                        for child in l.children:
                            def_list.append(child.text.strip())
                    ret.append(("defs", def_list))
                                     
                elif mode == "sdef":
                    sdef_list = []                
                    sdefs = content.findAll("li")
                    for sdefi in sdefs:
                        sdef_list.append(sdefi.text.strip())                   
                    ret.append(("sdefs", sdef_list))
                 
                elif mode == "eg":
                    sentences = content.findAll("li")
                    eg_list = []
                    for sentence in sentences:
                        eg_list.append(sentence.text.strip())
                    ret.append(("egs", eg_list))
        
        is_err = False
        ret = []
        
        contents = soup.findAll("div", {"class": "inner-box-wrapper"})
                
        header = contents[0]        
        has_wd, mode = mode_checker(header)
        if mode.startswith("err_"):
            is_err = True
        content_handler(header, has_wd, mode, ret, True)
        
        for content in contents[1:]:
            has_wd, mode = mode_checker(content)
            content_handler(content, has_wd, mode, ret)

        return is_err, json.dumps(ret)
        
    def pprint(self, translation):
        
        components = json.loads(translation)
        
        for component in components:
            if component[0] == "suggests":
                print self.tc.colorize("Did you mean:", "blue")
                for suggest in component[1]:
                    print "  " + suggest
            if component[0] == "fail":
                print self.tc.colorize(component[1], "red", "bold")
            if component[0] == "spelling":
                print "\n  ",
                print self.tc.colorize(component[1], "bold", "red")
            if component[0] == "attrs":
                print self.tc.colorize(component[1], "green") 
            if component[0] == "inflections":
                print self.tc.colorize(component[1], "green")   
            if component[0] == "sdefs":
                for sdefi in component[1]:
                    print self.tc.colorize(sdefi, "yellow")
            if component[0] == "defs":
                print self.tc.colorize("Def. ", "yellow", "bold")
                for defi in component[1]:
                    print " ",
                    spt = re.split(" [a-z] :\xa0", defi)
                    defi_re = spt[0]
                    if len(spt) > 1:
                        defi_re += " " + chr(97) + u" :\xa0" + spt[1]
                        for i in range(2, len(spt)):
                            defi_re += ("\n    " + chr(i + 96) + 
                                        u" :\xa0" + spt[i])
                    print self.tc.colorize(defi_re, "yellow")
            if component[0] == "egs":
                print self.tc.colorize("e.g. ", "blue", "bold")
                for eg in component[1]:
                    print " ",
                    print self.tc.colorize(eg, "blue", "underline")

