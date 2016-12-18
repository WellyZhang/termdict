#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
from basedict import BaseDict

class MWDict(BaseDict):

    """
    class: WMDict
        A subclass that inherits from BaseDict; implements technical details 
        for the Merriam-Webster web look-up parsing process.
    """
    
    def __init__(self):
    
        BaseDict.__init__(self, 
                          "http://www.merriam-webster.com/dictionary/",
                          "mw")
        
    def parse_web(self, soup):
        
        def has_word_header(inner_box):
            
            """
            Method: has_word_header
                check if the wrapper has a word header
            Params:
                inner-box
                  :: BeautifulSoup instance
                  :: the inner-box-wrapper in the web
            """ 
            
            if inner_box.find("div", {"class": "word-header"}) is not None:
                return True
            else:
                return False
        
        def mode_checker(inner_box, start=False):
        
            """
            Method: mode_checker
                examine the mode of the inner-box-wrapper
            Params:
                inner-box
                  :: BeautifulSoup instance
                  :: the inner-box-wrapper in the web
            """
            
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
                    if start:
                        mode = "hdef"
                else:
                    h2 = inner_box.h2.text.strip()
                    
                if h2.startswith("Definition") or \
                    h2.startswith("Full Definition") or \
                    h2.startswith("Medical Definition") or \
                    h2.startswith("Legal Definition"):
                    mode = "def"
                elif h2.startswith("Simple Definition"):
                    mode = "sdef"
                elif h2.startswith("Examples"):
                    mode = "eg"
                        
            return has_wd, mode
        
        def header_handler(content, main=False):
        
            """
            Method: header_handler
                extract word information in the header box
            Params:
                content
                  :: BeautifulSoup instance
                  :: the inner-box-wrapper in the web
                main
                  :: bool
                  :: if the content is the first inner-box-wrapper
            """
        
            spell = content.find("div", {"class": "word-header"})
            if main:
                spell = spell.h1.text.strip()
            else:
                spell = spell.h2.text.strip()
                
            attrs = content.find("div", {"class": "word-attributes"})
            attrs = " ".join(attrs.text.split())
                        
            return spell, attrs
         
        def content_handler(content, has_wd, mode, ret, main=False):
        
            """
            Method: content_handler
                extract word information in the wrapper box
            Params:
                content
                  :: BeautifulSoup instance
                  :: the inner-box-wrapper in the web
                has_wd
                  :: bool
                  :: if the box has a word header
                mode
                  :: str
                  :: the mode of the inner box
                ret
                  :: list
                  :: the returning structure; should be a list of tuples where
                     each tuple contains type and its contents
                     e.g. 
                       [("suggets", ["hello", "hull", "hell"]),
                        ("defs", ["ABC", "DEF", "GHI"])]
                main
                  :: bool
                  :: if the box is the first inner-box-wrapper
            """
            
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
                            # remove the "play" button
                            if "play" in text:
                                text.remove("play")
                            text = " ".join(text)
                            inflections += text + " "
                        ret.append(("inflections", inflections))                
                    
                    ct = content.find("div", {"class": 
                                "card-primary-content"})
                    
                    def_list = []

                    if ct:
                        lists = ct.findAll("li")
                        
                        for l in lists:
                            for child in l.children:
                                def_list.append(child.text.strip())
                    else:
                        lists = content.find("div", {"class":
                                    "definition-block def-text"}).findAll("li")
                        for l in lists:
                            def_list.append(l.text.strip())
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
        has_wd, mode = mode_checker(header, start=True)
        # error occurs on the first mode check
        if mode and mode.startswith("err_"):
            is_err = True
        content_handler(header, has_wd, mode, ret, True)
        
        for content in contents[1:]:
            has_wd, mode = mode_checker(content)
            content_handler(content, has_wd, mode, ret)

        # return a json-encoded string to be stored in the database
        
        return is_err, json.dumps(ret)
        
    def pprint(self, translation):
        
        components = json.loads(translation)
        
        # pretty-print based on the type of the component
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
                # structuring the output of definitions to be printed
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

