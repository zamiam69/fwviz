#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import fwviz.iptparser


if __name__ == '__main__':

	iptrules = sys.argv[1]
	fwviz.iptparser.iptParse(iptrules)

	sys.exit(0)

# vim:sts=4 sw=4 ts=4:
