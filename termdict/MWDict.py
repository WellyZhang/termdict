#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
from BaseDict import BaseDict

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
            if (msg is not None 
                and msg.text.strip().startswith("The word you've")):
                mode = "err"
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
            
            if mode == "err":
                suggests = content.findAll("a")
                sug_list = []
                for suggest in suggests:
                     sug_list.append(suggest.text.strip())
                ret.append(("suggests", sug_list))
                
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
                            inflections += child.text + " "
                        ret.append(("inflections", inflections))                
                    
                    content = content.find("div", {"class": 
                                "card-primary-content"})
                                
                    lists = content.findAll("li")
                    
                    for l in lists:
                        def_list = []
                        for child in l.children:
                            def_list.append(child.text.strip())
                        ret.append(("def_list", def_list))
                                     
                elif mode == "sdef":                
                    sdefs = content.find("div", 
                              {"class": "definition-block def-text"})
                    sdefs = " ".join(sdefs.text.split())
                    sdefs = "\n:".join(sdefs.split(":"))[1:]
                    ret.append(("sdefs", sdefs))
                 
                elif mode == "eg":
                    sentences = content.find("li")
                    eg_list = []
                    for sentence in sentences:
                        eg_list.append(sentence.text.strip())
                    ret.append(("egs", eg_list))
        
        is_err = False
        ret = []
        
        contents = soup.findAll("div", {"class": "inner-box-wrapper"})
                
        header = contents[0]        
        has_wd, mode = mode_checker(header)
        if mode == "err":
            is_err = True
        content_handler(header, has_wd, mode, ret, True)
        
        for content in contents[1:]:
            has_wd, mode = mode_checker(content)
            content_handler(content, has_wd, mode, ret)

        return is_err, json.dumps(ret)
        
    def pprint(self, translation):
        
        print "==="
        print translation
'''
                        if l.has_attr("class"):
                            verb = l.text.strip()
                            print verb
                        else:
                            definitions = ""
                            if l is not None:
                                for df in l.children:
                                    raw = " ".join(df.text.split()) + "\n"
                                    spt = re.split("[a-z] : ", raw)
                                    def_idx = spt[0]
                                    for i in range(1, len(spt)):
                                        def_idx += "\n " + chr(i + 96) + " : " + spt[i]
                                    if len(spt) > 1:
                                        definitions += def_idx[:-2]
                                    else:
                                        definitions += def_idx
                                print definitions
                        '''   

    
