#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module contains a variety of utility functions or classes.
"""

import ConfigParser

# Supplements of Basic Data Operations

def pops(pop_indexs, _list):
    """
    
    """
    pop_indexs = list(pop_indexs)
    pop_indexs.sort()
    pop_indexs.reverse()
    return [ _list.pop(pop_index) for pop_index in pop_indexs ]

class Config:
    """
    Config

    Config class defines a standard way for reading ini configuration file. Specifically
    speaking, an ini config file contains single or multiple sections, and a section also
    contains single or multiple options. 
	
	>>> conf = Config()
    >>> conf.get_section("SECTION_1")["OPTION_1"]
    """
    
    def __init__(self, ini_path):
        self.ini_path = ini_path
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(self.ini_path)

    def get_section(self, section):
    	"""
    	Get section
    	"""

        _dict = {}
        options = self.conf.options(section)
        for option in options:
            try:
                _dict[option] = self.conf.get(section, option)
                # if _dict[option] == -1:
                    # DebugPrint("skip: %s" % option)
            except:
                # print("exception on %s!" % option)
                _dict[option] = None
        return _dict