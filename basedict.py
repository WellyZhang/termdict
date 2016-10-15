#!/usr/bin/env python
# -*- coding: utf-8 -*-


import config
import os
import requests
import sqlite3
from bs4 import BeautifulSoup
from termcolors import TermColors


class BaseDict(object):
    
    def __init__(self, url, dbname):
    
        self.url = url
        dbpath = os.path.join(config.DIR, "termdict_{}.db".format(dbname))
        if os.path.exists(dbpath):
            self.db = sqlite3.connect(dbpath)
        else:
            os.mkdir(config.DIR)
            self.db = sqlite3.connect(dbpath)
            SQL = "CREATE TABLE dict" + \
                  "(word TEXT PRIMARY KEY NOT NULL, " + \
                  "content TEXT NOT NULL);"
            self.db.execute(SQL)
            self.db.commit()
        self.dbc = self.db.cursor()
        self.tc = TermColors()
    
    def translate(self, word):
        
        self.dbc.execute("SELECT content FROM dict where word=?", (word, ))
        content = self.dbc.fetchone()
        if content is None:
            soup = self.get_web(word)
            is_err, content = self.parse_web(soup)
            if not is_err:
                self.db.execute("INSERT INTO dict VALUES (?, ?)", 
                                (word, content))
                self.db.commit()
        else:
            content = content[0]
        self.pprint(content)
        
    def get_web(self, word):
        
        html = requests.get(self.url + word)
        soup = BeautifulSoup(html.text, "lxml")
        return soup
    
    def parse_web(self, resp):
        
        # elaborated in the subclasses         
        pass
        
    def pprint(self, structure):
        
        # elaborated in the subclasses
        pass
    
    def close(self):
        
        self.db.close()
        
