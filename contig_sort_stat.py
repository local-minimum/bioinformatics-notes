#!/usr/bin/env python

from matplotlib import pyplot as plt
import numpy as np
from Bio import SeqIO
import sys

#CHECK CLI ARGS
if len(sys.argv) < 3 or sys.argv[1][:2] == "-h" or sys.argv[1][:3] == "--h":

    print "\nBinning stats:"
    print "\n\tUSAGE: {0} [IN GROUP FAST FILE] [OUT GROUP FASTA FILE] (FORMAT)".format(
                sys.argv[0])

    print "FORMAT can be supplied as a string to look for other type of format"

    sys.exit()


FILE_FORMAT = "fastq"

if len(sys.argv) > 3:

    FILE_FORMAT = sys.argv[3].lower()
    
print "\n***STARTING stats extraction"

print "\n***PARSING in group file"

in_lens = list()

for seq_record in SeqIO.parse(sys.argv[1], FILE_FORMAT):

    in_lens.append(len(seq_record))

in_lens = sorted(in_lens, reverse=True)

print "\n***PARSING out group file"

out_lens = list()

for seq_record in SeqIO.parse(sys.argv[2], FILE_FORMAT):

    out_lens.append(len(seq_record))

out_lens = sorted(out_lens, reverse=True)

print "\n***Making pie graphs"

graph_path = sys.argv[1] + ".figures."

labels = ['In Group', 'Out Group']

fig = plt.figure()
ax = fig.gca()
ax.set_title("Contig Count Distribution")
sum_in = len(in_lens)
sum_out = len(out_lens)
fracs = np.array((sum_in, sum_out)) / float(sum_in + sum_out) * 100
explode = (0.05, 0)
ax.pie(fracs, explode=explode, labels=labels, autopct="%1.1f%%", shadow=True)
fig.savefig(graph_path+"count_pie.ps", format='ps')

fig = plt.figure()
ax = fig.gca()
ax.set_title("Sequence Length Distribution")
sum_in = sum(in_lens)
sum_out = sum(out_lens)
fracs = np.array((sum_in, sum_out)) / float(sum_in + sum_out) * 100
explode = (0.05, 0)
ax.pie(fracs, explode=explode, labels=labels, autopct="%1.1f%%", shadow=True)
fig.savefig(graph_path+"seq_len_pie.ps", format='ps')

print "\n***Calculating accumulative stuff"

joint_lens = sorted(in_lens + out_lens, reversed=True)

for s in (in_lens, out_lens, joint_lens):

    for i in xrange(1,len(s)):

        s[i] = s[i] + s[i-1]


print "\n***Extening for equal length"

max_l = max(map(len, (in_lens, out_lens, joint_lens)))

for s in (in_len, out_lens, joint_lens):

    if len(s) < max_l:

        s += [s[-1]] * (max_l - len(s))

print "\n***Making line graph"

labels.append("Total")
fig = plt.figure()
ax = fig.gca()
ax.set_title("Accumulative Sequence Lengths")
ax.plot([in_len, out_lens, joint_lens], labels=labels,
    aa=True)
ax.set_xticks([0, max_l])
ax.set_xticklabels([0, 100])
ax.set_xlabel("Percent of contigs")
ax.set_ylabel("Accumulative Sequence Length")
fig.savefig(graph_path+"acc_seq_len.ps", format='ps')

