#!/usr/bin/python

"""
Find all N sequences longer than supplied threshold in a FASTA-based file and plot if user wants to.
"""

from Bio import SeqIO
from argparse import ArgumentParser
from matplotlib import pyplot
import numpy as np
import re

parser = ArgumentParser(description='This script reports all stretches of N longer than a set threshold as a tabular output and/or a plot.')

parser.add_argument("-i", "--input-file", dest="inputfile", help="Sequence input file.", metavar="PATH")
parser.add_argument("-f", "--input-format", dest="inputfileformat", help="The format of the sequence file (fasta, fastq)", metavar="FORMAT")
parser.add_argument("-t", "--threshold", dest="threshold", type=int, default=100,  help="Threshold of minimum length consequtive N:s (default = 100)", metavar="X")
parser.add_argument("-m", "--motif", dest="motif", default="N", type=str, help="Motif to be repeated (default = N)")
parser.add_argument("-p", "--plot", dest="plot", default=True, type=bool, help="If set causes a plot of contig positions to be drawn.")
parser.add_argument("-c", "--plot-max-contigs", dest="max_contigs", default=-1, type=int, metavar="X", help="Sets the maximum number of contigs to plot (default unlimited)")
parser.add_argument("-a", "--hit-alpha", dest="hit_alpha", type=float, help="Set alpha value (0-1) for each marking on cont-plot. Default: 0.9", default=0.9, metavar="0.NN")
parser.add_argument("-w", "--hit-width", dest="hit_width", type=int, help="Set the width for the hit marking.  Default: 10", default=10, metavar="N")

parser.add_argument("-o", "--output-file", dest="outputfile", help="Path to output file to write data, if unset no output will be written.", metavar="PATH")

parser.add_argument("-v", "--verbose", dest="verbose", help="Makes the script tell you how far it has come (default = 0 (quiet))", default=0, type=int, metavar="N")
args = parser.parse_args()

known_alt_types = {'fa':'fasta', 'fq':'fastq'}

try:
    fs = open(args.inputfile)
except:
    parser.error("Couldn't locate inputfile")

if args.inputfileformat == None:

    args.inputfileformat = args.inputfile.split(".")[-1]

    if args.inputfileformat in known_alt_types.keys():
        args.inputfileformat = known_alt_types[args.inputfileformat]

if args.verbose == None:
    args.verbose = 0

if args.outputfile != None:
    try:
        fh = open(args.outputfile,'w')
    except:
        parser.error("Unable to create output file")

    fh.write('Id\tStart\tEnd\tSize\n')

 
else:
    fh = None

if args.plot == True:
    if args.hit_width == None:
        args.hit_width = 1000

    if args.hit_alpha == None:
        args.hit_alpha = 1.0

sequences = SeqIO.parse(args.inputfile,args.inputfileformat)

contig_i = 0
match_string = '(' + str(args.motif) + '){' + str(args.threshold) + ',}'

if 4 > args.verbose > 0:
    print "@Using regular expression: " + match_string

if args.verbose > 1:
    print 'Id\tStart\tEnd\tSize'

x_labels = []

for rec in sequences:

    contig_i += 1

    matches = re.finditer(match_string, str(rec.seq))
    #Graphworkds
    if args.plot == True and (args.max_contigs <= contig_i or args.max_contigs==-1):
        X = np.asarray([contig_i*2*args.hit_width, contig_i*2*args.hit_width])
        
        #Draw the contig length as it is
        pyplot.plot(X,np.asarray([0, len(rec.seq)]), 'g')

        x_labels.append(rec.id)

        for match in matches:

            pyplot.plot(X, np.asarray(match.span()),'r-', alpha=args.hit_alpha, linewidth=args.hit_width)
    
            if fh != None:

                fh.write(rec.id + "\t" + str(match.start()) + "\t" + \
                    str(match.end()) + "\t" + \
                    str(match.end() - match.start()) + '\n')

            if args.verbose > 1:
                print rec.id + "\t" + str(match.start()) + "\t" + \
                str(match.end()) + "\t" + \
                str(match.end() - match.start())

    elif fh != None:

        for match in matches:

            fh.write(rec.id + "\t" + str(match.start()) + "\t" + \
                str(match.end()) + "\t" + \
                str(match.end() - match.start()) + '\n')

            if args.verbose > 1:
                print rec.id + "\t" + str(match.start()) + "\t" + \
                str(match.end()) + "\t" + \
                str(match.end() - match.start())


    if 3 > args.verbose > 0:
        print "@Completed: " + str(rec.id)

if fh != None:
    fh.close()


if args.plot == True:

    pyplot.xticks(np.arange(1,len(x_labels)+1)*2*args.hit_width,x_labels)

    pyplot.show()


