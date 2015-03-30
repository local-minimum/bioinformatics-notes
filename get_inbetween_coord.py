#!/usr/bin/python

"""

This script takes parses a set of input files for 
coordinate information and acsession numbers, and 
downloads the sequence inbetween.

"""

### DEPENDENCIES

import os, sys
from time import time
from Bio import Entrez, SeqIO
from argparse import ArgumentParser


### RUN-TIME BEHAVIOUR

if __name__ == "__main__":

    #RECORD START TIME
    t = time()

    #SET-UP AND PARSE ARGUMENTS
    parser = ArgumentParser(description="The script compiles a list of"\
        + " sequences downloaded from NCBI using accesion ID and" \
        + " coordinates.")

    parser.add_argument('-a1', '--accesion-file1', type=str, metavar="PATH",\
        help="Path to the first file containing accession ID-list", dest="acc1")

    parser.add_argument('-a2', '--accesion-file2', type=str, metavar="PATH",\
        help="Path to the second file containing accession ID-list", dest="acc2")

    parser.add_argument("-1", type=str, metavar="PATH", dest="file_one",
        help="Path to first file containing coordinate info")

    parser.add_argument("-2", type=str, metavar="PATH", dest="file_two",
        help="Path to second file containing coordinate info")

    parser.add_argument("-o", "--output", type=str, metavar="PATH",
        help="Path output-file", dest="output")

    parser.add_argument("-e", "--e-mail", type=str, metavar="user@domain",
        help="E-mail for downloading sequences", dest="email")

    #CHECK THAT NECCESARY ARGUMENTS ARE SUPPLIED
    args = parser.parse_args()

    if args.acc1 is None or args.acc2 is None or \
        args.file_one is None or args.file_two is None:

        parser.error("All three input files must be specified")


    if args.email is None:
        parser.error("Can't do much if I don't get an email")
    else:
        Entrez.email = args.email

    #CHECK IF OUTPUT SHOULD BE PUT TO SCREEN OR FILE
    output_file_exists = True

    if args.output is None:
        output_file_exists = False

    #CHECK THAT ALL NECCESARY FILES ARE ACCESSIBLE
    try:
        fh_acc1 = open(args.acc1, 'r')
    except:
        parser.error("Unable to open accesion file 1")

    try:
        fh_acc2 = open(args.acc2, 'r')
    except:
        parser.error("Unable to open accesion file 2")

    try:
        fh_1 = open(args.file_one, 'r')
    except:
        parser.error("Unable to open coordinate file 1")

    try:
        fh_2 = open(args.file_two, 'r')
    except:
        parser.error("Unable to open coordinate file 2")

    if output_file_exists: 
        try:
            fh_out = open(args.output, 'w')
        except:
            parser.error("Unable create output file")

    print "*** READING FILES"

    #LOADING ALL THE FILES
    acc1 = fh_acc1.readlines()
    acc2 = fh_acc2.readlines()
    pos1 = fh_1.readlines()
    pos2 = fh_2.readlines()

    #CLOSING FILES
    fh_acc1.close()
    fh_acc2.close()
    fh_1.close()
    fh_2.close()

    print "*** BUILDING DICTIONARY"

    #CHECKING SO THAT THEY MAKE SENSE
    if len(acc1) * 2 != len(pos1) or len(acc2) * 2 != len(pos2):
        print len(acc1), len(pos1), len(acc2), len(pos2)
        parser.error("The coordinate files must have twice as many rows" \
            + " as do the accesion files, else it doesn't make sense")


    #COMPILING ALL GOOD RECORDS
    records = {}
    p1 = 0
    for a1 in acc1:
        p2 = 0
        for a2 in acc2:

            if a1 == a2:
                records[a1.strip('\n')] = sorted((int(pos1[p1*2].strip('\n')), 
                    int(pos1[p1*2 + 1].strip('\n')), 
                    int(pos2[p2*2].strip('\n')), 
                    int(pos2[p2*2 + 1].strip('\n'))))
                break

            p2 += 1
        p1 += 1

    print "Completed with " + str(len(records)) + " items in it"

    print "*** RETRIEVING SEQUENCES"

    #RETRIEVING SEQUENCES
    seqs_parsed = 0
    for key, sorted_coords in records.items():
 

        handle = Entrez.efetch(db="nucleotide", id=key.strip('\n'),
            rettype="gb")

        record = SeqIO.read(handle, "genbank")

        if output_file_exists:
            fh_out.write(">" + str(record.id) + "\n")
            fh_out.write(str(record.seq[sorted_coords[0]:sorted_coords[-1]]) + "\n")
        else:
            print ">" + str(record.id)
            print str(record.seq[sorted_coords[0]:sorted_coords[-1]])

        seqs_parsed += 1
        if seqs_parsed % 25 == 0:
            print "Gotten " + str(seqs_parsed) + " of " + str(len(records))

        #UNIT TEST START
        #if seqs_parsed > 3:
        #    break
        #UNIT TEST END

    print "*** Script completed in " + str(time() - t) + " seconds!"
