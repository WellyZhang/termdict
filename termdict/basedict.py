#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
from termcolors import TermColors
import config
import os
import requests
import sqlite3


class BaseDict(object):

    """
    class: BaseDict
        Super class of all sub-dictionaires; subclasses should inherit from
        this BaseDict and implement the parse_web method and pprint method.
    """  
    
    def __init__(self, url, name):
    
        """
        Method: __init__
            initialize the dictionary
        Params:
            url
              :: str
              :: URL of the web dictionary
            name
              :: str
              :: name of the dictionary
        """
             
        self.url = url
        dbpath = os.path.join(config.DIR, "termdict_{}.db".format(name))     
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
        
        """
        Method: translate
            look up the web dictionary for the word
        Params:
            word
              :: str
              :: the word to look up
        """
        
        # if in the database, do not parse the web
        self.dbc.execute("SELECT content FROM dict where word=?", (word, ))
        content = self.dbc.fetchone()
        if content is None:
            soup = self.get_web(word)
            is_err, content = self.parse_web(soup)
            # if err, do not insert it into the database
            if not is_err:
                self.db.execute("INSERT INTO dict VALUES (?, ?)", 
                                (word, content))
                self.db.commit()
        else:
            content = content[0]
            
        self.pprint(content)
        
    def get_web(self, word):
        
        """
        Method: get_web
            retrieve the web of the dictionary of the word
        Params:
            word
              :: str
              :: the word to look up in the web dictionary
        """
        
        html = requests.get(self.url + word)
        soup = BeautifulSoup(html.text, "lxml")
        return soup
    
    def parse_web(self, resp):
        
        """
        Method: parse_web
            elaborated in the subclasses         
        Params:
            resp
              :: BeautifulSoup instance
              :: the preprocessed web instance
        """
        
        pass
        
    def pprint(self, structure):
    
        """
        Method: pprint
            pretty-print the structured word information
            elaborated in the subclasses
        Params:
            structure
              :: str
              :: the structured word information
        """
        
        pass
    
    def close(self):
    
        """
        Method: close()
            close the database
        """
        
        self.db.close()
        
