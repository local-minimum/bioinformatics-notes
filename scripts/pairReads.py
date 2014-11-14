#!/usr/bin/env python

import sys

if len(sys.argv) < 4:
    print "USAGE: {0} delim file1 file2 [matching field]".format(sys.argv[0])
    sys.exit()


matchingField = 0
if len(sys.argv) == 5:
    matchingField = int(sys.argv[4])

print "Preparing"

f1 = set()
f2 = set()

try:
    fh1 = open(sys.argv[2], 'r')
except:
    print "Could not find first file"
    sys.exit()

try:
    fh2 = open(sys.argv[3], 'r')
except:
    print "Could not find second file"
    sys.exit()

p_paired = "{0}_paired.fq"
p_orphan = "{0}_orphan.fq"

delim = sys.argv[1]

print "Checking first file"

for r, line in enumerate(fh1):

    if r % 4 == 0:
        key = line.split(delim, 1)[matchingField]
        f1.add(key)

print "Done checking first file"

fh1.seek(0)

try:
    fh2_pair = open(p_paired.format(sys.argv[3]), 'w')
    fh2_orphan = open(p_orphan.format(sys.argv[3]), 'w')
except:
    print "Could not open second file's outputs {0}".format(
        (p_paired.format(sys.argv[3]), p_orphan.format(sys.argv[3])))
    sys.exit()

print "Checking and sorting second file"

for r, line in enumerate(fh2):
    if r % 4 == 0:
        key = line.split(delim, 1)[matchingField]
        f2.add(key)
        if key in f1:
            o_file = fh2_pair
        else:
            o_file = fh2_orphan

    o_file.write(line)

fh2_pair.close()
fh2_orphan.close()
fh2.close()
del f1
print "Done checking and sorting second file"

print "Sorting first file"
try:
    fh1_pair = open(p_paired.format(sys.argv[2]), 'w')
    fh1_orphan = open(p_orphan.format(sys.argv[2]), 'w')
except:
    print "Could not open first file's outputs"
    sys.exit()

for r, line in enumerate(fh1):

    if r % 4 == 0:
        key = line.split(delim, 1)[matchingField]
        if key in f2:
            o_file = fh1_pair
        else:
            o_file = fh1_orphan

    o_file.write(line)

print "Done!"

