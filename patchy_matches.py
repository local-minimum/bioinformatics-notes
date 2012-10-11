#!/usr/bin/env python

import sys
import os
from Bio.Blast import NCBIXML
from scipy.signal import convolve
import numpy as np
from matplotlib import pyplot as plt

#SIMPLE HELP
if len(sys.argv) < 2 or sys.argv[1][:2] == "-h" or sys.argv[1][:3] == "--h":

    print "\nSimple binning algorithm for contigs"
    print "\n\tUSAGE: {0} [INPUT XML FILE] (FILTER FILE)".format(sys.argv[0])

    sys.exit()

try:

    fh = open(sys.argv[1], 'r')

except:

    print "Can't open {0}".format(sys.argv[1])

    sys.exit()

blast_records = NCBIXML.parse(fh)
FASTA_HEADER = '>'
my_filt = None

if len(sys.argv) > 2:

    try:
        fh2 = open(sys.argv[2], 'r')
    except:
        fh2 = None

    if fh2 is not None:
        
        my_filt = list()
        for line in fh2:
            if line[0] == FASTA_HEADER:

                my_filt.append(line[1:].strip())

        fh2.close()

vals = list()
names = list()

row = 0

for blast_record in blast_records:

    l = blast_record.query_letters
    m = np.zeros((l,))

    if my_filt is None or blast_record.query in my_filt:

	names.append(blast_record.query)

        for al in blast_record.alignments:

            for hsp in al.hsps:

                #ADD: filter if you are good enough?

                m[hsp.query_start: hsp.query_end] = 1

        #Measure binary string entropy
        p = m.sum() / float(l)
        if p == 1:
            Hx_1 = 0
            Hx_2 = 0
        elif p == 0:
            Hx_1 = 1
            Hx_2 = 1
        else:
            Hx_1 = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
            #Edges
            m = np.abs(convolve(m, [-1, 1]))
            p = np.power(m.sum() / float(l), 1/2.)
            Hx_2 = -p * np.log2(p) - (1 - p) * np.log2(1 - p)

        vals.append((Hx_1, Hx_2))

    if row % 500 == 0 and len(vals) > 0:

        print "Contig {0} had patchyness {1}".format(row, vals[-1])

    row += 1

fh.close()

vals = np.array(vals)

#Save array
np.save('{0}_entropy.npy'.format(sys.argv[1]), vals)

#Calculate patchyness
vals[np.isnan(vals)] = 1
vals = np.sqrt(vals.prod(1))

#Save per contig value
fh = open('{0}_entropy.csv'.format(sys.argv[1]), 'w')
for l, v in zip(names, vals):
    fh.write("{0}\t{1}\n\r".format(l, v))

fh.close()

#Draw figure
fig = plt.figure()
ax = fig.gca()
ax.hist(vals, bins=100)
ax.set_title("Patchyness Distribution")
ax.set_xlabel("<- 0 Simple Match,  Complex/Non-Match 1->")
fig.savefig("{0}_entropy.ps".format(sys.argv[1]), format="ps")

