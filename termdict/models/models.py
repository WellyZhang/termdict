#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import requests
import sqlite3
from bs4 import BeautifulSoup


class BaseDict(object):
    
    def __init__(self, url):
    
        self.url = url
        # TODO: connect a database
    
    def translate(self, word):
        
        # TODO: if word in the database
        resp = self.get_web(word)
        ret = self.parse_web(resp)
        
        return None
        # TOOD: insert one record to the database
            
        # pprint(ret)
    
    def get_web(self, word):
        
        html = requests.get(self.url + word)
        soup = BeautifulSoup(html.text, "lxml")
        return soup
    
    def parse_web(self, resp):
        
        return None
        
    def pprint(self, structure):
        
        return None
        

class MWDict(BaseDict):
    
    def __init__(self):
    
        BaseDict.__init__(self, "http://www.merriam-webster.com/dictionary/")
        
    def parse_web(self, soup):
        
        def has_word_header(inner_box):
            
            if inner_box.find("div", {"class": "word-header"}) is not None:
                return True
            else:
                return False
        
        def mode_checker(inner_box):
            
            msg = inner_box.find("div", {"class": "card-primary-content"})
            msg = msg.text.strip()
            has_wd = None
            mode = None
            if msg.startswith("The word you"):
                mode = "err"
            else:            
                has_wd = has_word_header(inner_box)
                mode = None
                if has_wd:
                    h2 = inner_box.find("div", {"class": "word-sub-header"})
                    h2 = h2.text.strip()
                    if h2.startswith("Definition") or \
                        h2.startswith("Full Definition") or \
                        h2.startswith("Medical Definition"):
                        mode = "def"
                    elif h2.startswith("Simple Definition"):
                        mode = "sdef"
                else:
                    h2 = inner_box.h2.text.strip()
                    if h2.startswith("Examples"):
                        mode = "eg"
                    elif h2.endswith("Synonyms"):
                        mode = "syno"
                    elif h2.startswith("Definition") or \
                        h2.startswith("Full Definition") or \
                        h2.startswith("Medical Definition"):
                        mode = "def"
                        
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
        
        
        def content_handler(content, has_wd, mode, main=False):
            
            if mode == "err":
                suggests = content.findAll("a")
                for suggest in suggests:
                    print suggest.text.strip()
            else: 
                if has_wd:
                    header = header_handler(content, main)
                    print header
                    print "-------"          
                
                if mode == "def":
                
                    inflections = content.find("span", {"class": "inflections"})
                    if inflections is not None:
                        children = inflections.children
                        inflections = ""
                        for child in children:
                            inflections += child.text + " "
                        print inflections                
                    
                    content = content.find("div", {"class": 
                                "card-primary-content"})
                                
                    lists = content.findAll("li")
                    
                    for l in lists:
                        for child in l.children:
                            print child.text.strip()
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
                elif mode == "sdef":                
                    defs = content.find("div", 
                              {"class": "definition-block def-text"})
                    defs = " ".join(defs.text.split())
                    defs = "\n:".join(defs.split(":"))[1:]
                    print defs
                
                elif mode == "eg":
                    sentences = content.find("li")
                    print "======"
                    for sentence in sentences:
                        print sentence.text.strip()
                 
                elif mode == "syno":
                    synos = content.find("div", 
                               {"class": "card-primary-content"})
                    synos = synos.div
                    print "******"
                    for syno in synos:
                        if syno.name == "h6" or syno.name == "a":
                            print syno.text.strip()

        contents = soup.findAll("div", {"class": "inner-box-wrapper"})
                
        header = contents[0]        
        has_wd, mode = mode_checker(header)
        ret_header = content_handler(header, has_wd, mode, True)
        
        for content in contents[1:]:
            has_wd, mode = mode_checker(content)
            ret_child = content_handler(content, has_wd, mode)
         
        
        return ""
        
    def pprint(self, translation):
    
        return None                
                  
if __name__ == "__main__":
    
    s = MWDict()
    t = s.translate("cabbage")
    t = s.translate("honey")
    t = s.translate("terrible")    
        
        
