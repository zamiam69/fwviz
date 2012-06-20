# -*- coding: utf-8 -*-
"""
Created on Apr 23, 2012

@author: maz
"""

from simpleparse.parser import Parser
from simpleparse import dispatchprocessor


iptablesGrammar = """
tablesection    := (comment*, tableline, comment*, chainline+, ruleline+)
<comment>        := [#], -[\n]*, nl
tableline        := '*', tablename, nl
tablename        := 'mangle'/'nat'/'filter'/'raw'/'security'
chainline        := ':', chainname, ts, defaultpolicy, ts, counters, nl
chainname        := [A-Za-z], [a-zA-Z0-9_-]*
defaultpolicy    := 'DROP'/'ACCEPT'/'REJECT'/'-'
counters        := '[', [0-9]*, ':', [0-9]*, ']'
ruleline        := rule, nl
<nl>            := [\n]
<ts>            := [ \t]*
shortopt        := '-', [a-zA-Z]
longopt            := '--', [0-9a-zA-Z-]+
opt                := longopt/shortopt
optarg            := opt, ts, (negarg / arg)

rule            := rulecommand, (ts, optarg)*, ts?

rulecommand        := opt, ts, chainname, (ts, ruleindex)?
ruleindex        := [1-9], [0-9]*
rulespec1        := match*, ts, target*
match            := -[\n]*
target            := '-j'/'--jump', ts, chainname, ts, targetopt*
targetopt        := -[\n]*

arg                    :=  literal / -[\\"\\' \t\n]+
negarg                := '!', ts, arg
literal             :=  ("'",(CHARNOSNGLQUOTE/ESCAPEDCHAR)*,"'")  /  ('"',(CHARNODBLQUOTE/ESCAPEDCHAR)*,'"')
CHARNOSNGLQUOTE     :=  -[\\']+
CHARNODBLQUOTE      :=  -[\\"]+
ESCAPEDCHAR         :=  '\\',( SPECIALESCAPEDCHAR / OCTALESCAPEDCHAR )
SPECIALESCAPEDCHAR  :=  [\\abfnrtv]
OCTALESCAPEDCHAR    :=  [0-7],[0-7]?,[0-7]?
"""


class IptProcessor(dispatchprocessor.DispatchProcessor):
    """Processor class for iptables-save dumps"""

    def tableline(self, tup, prsbuf):
        print "###", tup[3][0]
        self.table = dispatchprocessor.dispatch(self, tup[3][0], prsbuf)

    def tablename(self, tup, prsbuf):
        return repr(dispatchprocessor.getString(tup, prsbuf))

    def chainline(self, tup, prsbuf):
        print repr(dispatchprocessor.getString(tup, prsbuf))

    def chainname(self, tup, prsbuf):
        return repr(dispatchprocessor.getString(tup, prsbuf))

    def defaultpolicy(self, tup, prsbuf):
        return repr(dispatchprocessor.getString(tup, prsbuf))

    def counters(self, tup, prsbuf):
        return repr(dispatchprocessor.getString(tup, prsbuf))

    def ruleline(self, tup, prsbuf):
        rule = dispatchprocessor.dispatch(self, tup[3][0], prsbuf)
        fw.fromParser(rule)

    def rulecommand(self, tup, prsbuf):
        return dispatchprocessor.dispatchList(self, tup[3], prsbuf)

    def rule(self, tup, prsbuf):
        return dispatchprocessor.dispatchList(self, tup[3], prsbuf)

    def arg(self, tup, prsbuf):
        return repr(dispatchprocessor.getString(tup, prsbuf))

    def negarg(self, tup, prsbuf):
        return repr(dispatchprocessor.getString(tup, prsbuf))

    def opt(self, tup, prsbuf):
        return repr(dispatchprocessor.getString(tup, prsbuf))

    def optarg(self, tup, prsbuf):
        return dispatchprocessor.dispatchList(self, tup[3], prsbuf)
