#!/usr/bin/python

import sys, os

if len(sys.argv) < 3:
    print "\nUSAGE:\t" + str(sys.argv[0]) + " [Prepend-string] [Filepatterns]"
    print "\t(Please note that you might want a space in the end of"
    print "\tprepended-string)"
    print "\n\nOUTPUT:\tA space separated list or prepended prepend-strings"
    print "\tand to the files matching the pattern(s)\n"

else:

    for a in sys.argv[2:]:

        print sys.argv[1] + a,

    print
