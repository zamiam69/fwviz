"""
Created on Sep 18, 2012

@author: maz

For a german glade tutorial see 
    http://www.florian-diesch.de/doc/python-und-glade/online/einfaches-programm.html
"""

import gtk

class FwViz(object):
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("fvwiz.glade")
        self.builder.connect_signals(self)
        
        self.path = None
        