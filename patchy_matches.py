#!/usr/bin/env python

import sys
import os
from Bio.Blast import NCBIXML
from scipy.signal import convolve
import numpy as np
from matplotlib import pyplot as plt

def patchyness(m):

    #Measure binary string entropy
    p = m.sum() / float(l)
    if p == 1:
        Hx = 1
        #Hx_2 = 0
    elif p == 0:
        Hx = 0
        #Hx_2 = 1
    else:
        """
        Hx_1 = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
        """
        #Edoges
        m = np.abs(convolve(m, [-1, 1]))
        p2 = m.sum() / float(l)
        Hx = 1 - (-p2 * np.log2(p2) - (1 - p2) * np.log2(1 - p2))

    return p, Hx

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
lengths = list()
names = list()

row = 0

for blast_record in blast_records:

    l = blast_record.query_letters
    m = np.zeros((l,))

    if my_filt is None or blast_record.query in my_filt:

        names.append(blast_record.query)
	lengths.append(blast_record.query_length)

        for al in blast_record.alignments:

            for hsp in al.hsps:

                #ADD: filter if you are good enough?

                m[hsp.query_start: hsp.query_end] = 1


        vals.append(patchyness(m))

    if row % 500 == 0 and len(vals) > 0:

        print "Contig {0} had patchyness {1}".format(row, vals[-1])

    row += 1

fh.close()

vals = np.array(vals)

#Save array
np.save('{0}_patchy.npy'.format(sys.argv[1]), vals)

#Calculate patchyness
vals = np.sqrt(vals.prod(1))

#Save per contig value
fh = open('{0}_patchy.csv'.format(sys.argv[1]), 'w')
for l, v in zip(names, vals):
    fh.write("{0}\t{1}\n\r".format(l, v))

fh.close()

#Draw figure
fig = plt.figure()
fig.subplots_adjust(hspace = .4)

fig.suptitle(sys.argv[1], fontsize=16)

ax = fig.add_subplot(2,1,1)
ax.hist(vals, bins=100)
ax.set_title("Patchyness Distribution")
ax.set_xlabel("<- 0 Complex/Non-Match -- Simple/Good Match 1->")

ax = fig.add_subplot(2,1,2)
ax.set_title('Patchyness vs Contig Length')
ax.semilogx(lengths, vals, '+', basex=10)
ax.set_xlabel('Log10 Length of Contig')
ax.set_ylabel('Patchyness (same scale as above)')

fig.savefig("{0}_patchy.ps".format(sys.argv[1]), format="ps")
