#!/usr/bin/env python

import sys
import os
from Bio.Blast import NCBIXML
import numpy as np
from scipy.stats import ttest_ind


def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


def report_progress(i, tot, f=300):

    if i % f == 0:
        print "{0:.1f}%\r".format(i*100/tot)
        sys.stdout.flush()


def get_top_3_scores(blast_records):

    ret_dict = {}

    for i, blast_record in enumerate(blast_records):

        l = []
        #TOP 3 hits
        for al in blast_record.alignments[:(len(blast_record.alignments) > 3 
                and 4 or len(blast_record.alignments))]:

            l.append(al.hsps[0].score)

        if len(l) > 0:
            ret_dict[al.title] = l

    return ret_dict


def assign_contigs(set_A, set_B, alpha=0.01):

    all_keys = uniq(set_A.keys() + set_B.keys())
    tot = float(len(all_keys))

    for i, k in enumerate(all_keys):

        if k in set_A and k in set_B:

            in_set = np.array(set_A[k])
            out_set =  np.array(set_B[k])

            s = ttest_ind(in_set, out_set)[1]

            #print s, alpha, np.mean(out_set), np.mean(in_set)

            if s < alpha and out_set.mean() > in_set.mean():

                del set_A[k]

            elif np.isnan(s) and (out_set.mean() - in_set.mean()) \
                    / in_set.mean() > 0.5:

                del set_A[k]

            else:

                del set_B[k]

        report_progress(i, tot)

    return set_A, set_B


def test_dupe_keys(set_A, set_B):

    for k in set_A:

        if k in set_B:

            return True

    return False


#SIMPLE HELP
if len(sys.argv) < 4 or sys.argv[1][:2] == "-h" or sys.argv[1][:3] == "--h":

    print "\nSimple binning algorithm for contigs"
    print "\n\tUSAGE: {0} [IN GROUP] [OUT GROUP] [FASTA FILE] (FORMAT)".format(sys.argv[0])
    print "\n\nWhere both in and out group should be NCBI compatible"
    print "BLAST outputs."
    print "\nThe FASTA-file should be the file that was blasted against both"
    print "databases."
    print "FORMAT can be either 'fasta' or 'fastq' (def: 'fasta')"

    sys.exit()

print "\n***STARTING BINNING SCRIPT"

REQ_CHR = ">"
FILE_FORMAT = 'fasta'

if len(sys.argv) > 4:

    if sys.argv[4].lower() == "fastq":

        REQ_CHR = "@"
        FILE_FORMAT = 'fastq'

print "\n***CHECKING all input files"

#CHECKING SO FILES EXISTS BEFORE PARSING
fh = []

for i in xrange(3):

    try:
        fs = open(sys.argv[i+1], 'r')
    except:
        print "Failed to open BLAST report file '{0}'".format(sys.argv[1+i]),
        print " for {0}".format(['in group', 'out group','fasta file'][i])
        sys.exit()

    fh.append(fs)

print "\n***ANALYSING in group results"

#PARSING FILES
blast_records = NCBIXML.parse(fh[0])
in_dict = get_top_3_scores(blast_records)
fh[0].close()


print "\n***ANALYSING out group results"

blast_records = NCBIXML.parse(fh[1])
out_dict = get_top_3_scores(blast_records)
fh[1].close()

print "\n***ASSIGNING contigs to either set"

in_dict, out_dict = assign_contigs(in_dict, out_dict)

print "IN DICT len: {0}".format(len(in_dict.keys()))
print "OUT DICT len: {0}".format(len(out_dict.keys()))

"""
print "\n***VERIFYING assignment"

#MAKE SURE THERE ARE NO DUPLICATES
if test_dupe_keys(in_dict, out_dict):

    print "ERROR: Some keys are in both sets, this should not be"
    sys.exit()

"""

print "\n***SETTING output file names"

check_safe_name = False
uniquefier = 0
base_path = sys.argv[3].split(os.sep)[-1] + "."

while check_safe_name == False:

    in_path = base_path + "{0}.in_group.{1}".format(uniquefier, FILE_FORMAT)
    out_path = base_path + "{0}.out_group.{1}".format(uniquefier, FILE_FORMAT)

    try:

        fs = open(in_path, 'r')
        fs.close()

    except:

        try:

            fs = open(out_path, 'r')
            fs.close()

        except:

            check_safe_name = True 

    if not check_safe_name:

        uniquefier += uniquefier

try:

    write_file = {'in': open(in_path,'w'), 'out': open(out_path, 'w')}

except:

    print "ERROR: Could not open output files ({0})!".format((in_path, out_path))
    sys.exit()

print "\n***BINNING contigs into output files"

fs = fh[-1]
req = list()

for line in fs:

    if line[0] == REQ_CHR:

        if len(req) > 0:

            #Write previous line to where it belongs
            
            if req[0] in out_dict:

                write_file['out'].write("\n\r".join(req))

            else:

                write_file['in'].write("\n\r".join(req))

        req = list()

    req.append(line)

#Closing files
fh[-1].close()
for f in write_file:

    write_file[f].close()

print "\n***DONE binning contigs"
print "IN GROUP: {0}".format(in_path)
print "OUT GROUP: {0}".format(out_path)
