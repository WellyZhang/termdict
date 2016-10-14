#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import requests
import sqlite3

class BaseDict(object):
    
    def __init__(self, url, dbname):
    
        self.url = url
        if os.path.exists("~/.termdict/termdict_{}.db".format(name)):
            self.db = sqlite3.connect("~/.termdict/termdict_?.db", (name, ))
            
        else:
            os.path.mkdir("~/.termdict")
            self.db = sqlite3.connect("~/.termdict/termdict_?.db", (name, ))
            SQL = "CREATE TABLE dict" + \
                  "(word TEXT PRIMARY KEY NOT NULL, " + \
                  "content TEXT NOT NULL);"
            self.db.execute(SQL)
            self.db.commit()
        self.dbc = self.db.cursor()
    
    def translate(self, word):
        
        self.dbc.execute("SELECT content FROM dict where word=?", (word, ))
        content = self.dbc.fetchone()
        if content is None:
            soup = self.get_web(word)
            content = self.parse_web(soup)
            self.dbc.execute("INSERT INTO dict VALUES (?, ?)", (word, content))
        pprint(content)
        
    def get_web(self, word):
        
        html = requests.get(self.url + word)
        soup = BeautifulSoup(html.text, "lxml")
        return soup
    
    def parse_web(self, resp):
        
        # defined in the subclasses         
        return None
        
    def pprint(self, structure):
        
        # defined in the subclasses
        return None
    
    def close(self):
        
        self.db.close()
