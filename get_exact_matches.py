#!/usr/bin/python

"""
FINDS ALL OCCURANCES OF A PATTERN IN A FASTA FILE
KNOWS SHORTCUTS 'EcoR1' AS PATTERN.

"""

### DEPENDENCIES

import sys, os
from Bio import SeqIO
from argparse import ArgumentParser

### RESULTS CLASS

class RE_positions():

    def __init__(self, restriction_enzymes):

        self._RE_list = restriction_enzymes
        self._histogram = None

        self.fresh_start()

    def fresh_start(self):

        self._results = {}
        for RE in self._RE_list:
            self._results[RE] = {}

    def add(self, RE, seq_id, seq_pos):
        self.last = seq_pos
        if seq_pos >= 0:
            try:
                self._results[RE][seq_id].append(seq_pos)
            except KeyError:
                self._results[RE][seq_id] = [seq_pos]

    def histogram(self):
        self._histogram = {}

        for key, item in self._results.items():
            distances = {}
            for hits in item.values():
                if len(hits) > 1:
                    for i in xrange(len(hits)-1):
                        try:
                            distances[str(hits[i+1]-hits[i])] += 1
                        except:
                            distances[str(hits[i+1]-hits[i])] = 1

            self._histogram[key] = distances

        return self._histogram

    def get_positions(self):
        return self._results

    def print_stats(self):
        for key, item in self._results.items():
            c = 0
            for pos in item.values():
                c += len(pos)

            print "@ Cut site " + str(key) + " appears in " + str(len(item)) + " contigs a total of " + str(c) +  " times"

common_re = {'EcoR1': 'GAATTC', 'Cla1':'ATCGAT', 'BamH1': 'GGATCC', 'BglII': 'AGATCT', 'Dra1': 'TTTAAA', 'EcoRV':'GATATC', 'HindIII':'AAGCTT', 'Pst1':'CTGCAG','SalI': 'GTCGAC', 'SmaI':'CCCGGG', 'XmaI':'CCCGGG'}

parser = ArgumentParser(description='This script will eventually give you all restriction enzyme hits')
parser.add_argument("-i", "--input-file", dest="inputfile", help="Sequence input file to cut in.", metavar="FILE")
parser.add_argument("-f", "--input-format", default="", dest="inputformat", help="Specify the input format (fasta, fastq), if not" + \
    " supplied it will be inferred from file-ending.", metavar="FORMAT")
parser.add_argument("-r", "--restriction-sequence", dest="patterns", help="Comma-separated list of restriction enzyme patterns, or enzyme names " + str(common_re.keys()), metavar="PATTERN(S)")
args = parser.parse_args()

'''
if  > 0:
    for a in args:
        print "WARNING, " + str(a) + " IS NOT INCLUDED SINCE IT'S NOT AN OPTION"
'''



if args.inputformat == "":

    try:
        args.inputformat = str(args.inputfile.split(".")[-1])
    except:
        parser.print_help()
        parser.error("Could not infer file-type from suffix")

try:
    patterns = args.patterns.split(",")
except:
    parser.print_help()
    parser.error("Bad restriction patterns!")

for i, p in enumerate(patterns):
    if p in common_re.keys():
        patterns[i] = common_re[p]

try:
    sequences = SeqIO.parse(args.inputfile,args.inputformat)
except: 
    parser.print_help()
    parser.error("Bad number of arguments or file doesn't exist... come on!")

print "@ Data for %s " % args.inputfile
#print "It has " + str(len(sequences)) + " entries."

re_positions = RE_positions(patterns)
bp = 0
contig_lengths = {}

contigs = 0
for rec in sequences:
    bp += len(rec.seq)
    contig_lengths[str(rec.id)] = len(rec.seq)
    contigs += 1
    for re in patterns:
        re_positions.last = 0
        while re_positions.last >= 0: 
            #print dir(rec)
            re_positions.add(re, rec.id ,rec.seq.find(re, start = re_positions.last))
            if re_positions.last >= 0:
                re_positions.last += 1
            else:
                break
print "@", contigs, "contigs analysed (total of", bp, "bp)."
re_positions.print_stats()

print re_positions.histogram()
print re_positions.get_positions()
print contig_lengths

#!/usr/bin/python
