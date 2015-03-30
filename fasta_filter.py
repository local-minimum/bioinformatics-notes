#!/usr/bin/python

"""

This script takes parses a fasta file and keeps all
records that fall within the thresholds

"""

### DEPENDENCIES

#import os, sys
from time import time
from argparse import ArgumentParser

# RUN-TIME BEHAVIOUR

t = time()

#MAKING THE ARGUMENT PARSER
parser = ArgumentParser(description="This script parses a fasta file"\
    + " and keeps all records that fullfills the set thresholds")

parser.add_argument('-i', '--input', help="Input file to parse, default 0", 
    metavar="PATH", dest="input", type=str)

parser.add_argument('-o', '--output', help="Output file to place all " +\
    "records that passed the test, if not specified it will be put to "+\
    "STOUT", metavar="PATH", dest="output", type=str)

parser.add_argument('-l', '--lower', help="The lower threshold"+\
    " which the sequence length must be above or equal to.", metavar="N", 
    type=int, dest="low")

parser.add_argument('-u', '--upper', help="The upper threshold below "+\
    "which the sequence length must be. For unlimited upper value, omit this", 
    metavar="N", type=int, dest="high")

args = parser.parse_args()

#CHECKING THE FILES
if args.input is None:

    parser.error("The input file must be supplied")

has_output_file = True
if args.output is None:
    has_output_file = False

try:
    fh = open(args.input, 'r')
except:
    parser.error("Error opening the input file")

if has_output_file:
    try:
        fh_out = open(args.output, 'w')
    except:
        parser.error("Error opening the output file")

#CHECKING LOWER THRESHOLD
if args.low is None:
    args.low = 0

#PREPARATIONS
fasta_header = ""
records_parsed = 0
seq_data = ""
seq_len = 0
in_record = False
len_max = 0
len_min = -1
records_kept = 0

#GOING THROUGH THE FILE
for line in fh:

    if line[0] == ">":

        fasta_header = line

        if in_record:

            if args.low <= seq_len and (args.high is None or \
                args.high > seq_len):

                records_kept += 1
                if seq_len > len_max:
                    len_max = seq_len
                elif seq_len < len_min or len_min == -1:
                    len_min = seq_len

                if has_output_file:

                    fh_out.write(fasta_header)
                    fh_out.write(seq_data)

                    if records_parsed % 100 == 0:
                        print "Parsed " + str(records_parsed) + " records."
                else:
                    print fasta_header.strip("\n")
                    print seq_data.strip("\n")

        seq_data = ""
        seq_len = 0
        in_record = True

    elif in_record:
        seq_data += line
        seq_len += len(line.strip("\n"))
    else:
        in_record = False

    records_parsed += 1
 
if in_record:

    if args.low <= seq_len and (args.high is None or \
        args.high > seq_len):

        if has_output_file:

            fh_out.write(fasta_header)
            fh_out.write(seq_data)

            print "Parsed " + str(records_parsed) + " records."
            print "Kept " + str(records_kept) + " records."
            print "Shortest record kept: " + str(len_min)
            print "Longest record kept: " + str(len_max)
        else:
            print fasta_header.strip("\n")
            print seq_data.strip("\n")

fh.close()
if has_output_file:
    fh_out.close()
    print "Run-time: " + str(time() - t) + " seconds"

