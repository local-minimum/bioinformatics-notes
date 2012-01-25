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

parser.add_argument("-p", "--plot", dest="plot", default=True, type=bool, help="If set causes a plot of contig positions to be drawn.")
parser.add_argument("-m", "--plot-max-contigs", dest="max_contigs", default=-1, type=int, metavar="X", help="Sets the maximum number of contigs to plot (default unlimited)")
parser.add_argument("-a", "--hit-alpha", dest="hit_alpha", type=float, help="Set alpha value (0-1) for each marking on cont-plot. Default: 0.1", default=0.1, metavar="0.NN")
parser.add_argument("-w", "--hit-width", dest="hit_width", type=int, help="Set the width for the hit marking.  Default: 10", default=10, metavar="N")

parser.add_argument("-o", "--output-file", dest="outputfile", help="Path to output file to write data, if unset no output will be written.", metavar="PATH")

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

if args.outputfile != None:
    try:
        fh = open(args.outputfile,'w')
    except:
        parser.error("Unable to create output file")
else:
    fh = None

if args.plot == True:
    if args.hit_width == None:
        args.hit_width = 1000

    if args.hit_alpha == None:
        args.hit_alpha = 1.0

sequences = SeqIO.parse(args.inputfile,args.inputfileformat)

contig_i = 0
match_string = 'N{' + str(args.threshold) + ',}'

print match_string

for rec in sequences:

    contig_i += 1

    match_object = re.search(match_string, str(rec.seq))
    #Graphworkds
    if args.plot == True and (args.max_contigs <= contig_i or args.max_contigs==-1):
        X = np.asarray([contig_i*2*args.hit_width, contig_i*2*args.hit_width])
        
        #Draw the contig length as it is
        pyplot.plot(X,np.asarray([0, len(rec.seq)]), 'g')

        if match_object != None:
            if match_object.lastindex != None:
                for hit in range(match_object.lastindex):
                    pyplot.plot(X, np.asarray([match_object.start(hit), match_object.stop(hit)]),'r-', alpha=args.alpha)
            
                    if fh != None:

                        fh.writeline(req.id + str(match_object.start(hit)) + "\t" + str(match_object.stop(hit)) + "\t" + str(match_object.stop(hit) - match_object.start(hit)))

    elif fh != None and match_object != None:
        if match_object.lastindex != None:
            for hit in range(match_object.lastindex):
        
                if fh != None:

                    fh.writeline(req.id + str(match_object.start(hit)) + "\t" + str(match_object.stop(hit)) + "\t" + str(match_object.stop(hit) - match_object.start(hit)))



if fh != None:
    fh.close()


if args.plot == True:

    pyplot.show()

'''



if args.plot == "dist":

    color_pos = 0
    color_order = "rgbcmyk"
    if args.markerchar == None:
        args.markerchar = color_order[color_pos] + '-'

    for pattern in patterns:
        if pattern in results_dict.keys():
            X = np.asarray(map(int, results_dict[pattern]))
            if color_pos > 0:
                args.markerchar = color_order[color_pos/len(color_order)] + args.markerchar[-1]


            if args.low != None:
                low = int(args.low)
            else:
                low = np.min(X)

            if args.high != None:
                high = int(args.high)
            else:
                high = np.max(X)

            X_filter = np.where(np.logical_and(low <= X, X <= high), True, False)
            X_filtered = X[X_filter]
            X_sorter = np.argsort(X_filtered)
            Y = np.asarray(results_dict[patterns[0]].values())
            Y_filtered = Y[X_filter]

            pyplot.plot(X_filtered[X_sorter], Y_filtered[X_sorter], args.markerchar, markersize=args.markersize)
        else:
            print "Pattern", pattern, "is not in parse list"

elif args.plot == "cont":
    if args.low != None and args.high != None:
        if len(patterns) > 1:
            print "This graph only supports one pattern so far (using first)"
        low = int(args.low)
        high = int(args.high)

        contig_i = 0
        x_labels = []
        for contig in pos_dict[patterns[0]].keys():
            contig_i += 1
            x_labels.append(contig)
            Y =  np.asarray(pos_dict[patterns[0]][contig])
            Y_diff = Y[1:]-Y[:-1]
            Y_filtered = np.where(np.logical_and(low <= Y_diff, Y_diff <= high),True, False)
            Y = Y[Y_filtered]


            X = np.ones(Y.shape)* contig_i

            pyplot.plot(np.asarray([contig_i, contig_i]), np.asarray([0,contig_dict[contig]]), 'g-', alpha=1)
            #if len(X) > 2:
            #    Y_sizes = np.exp(-(Y[2:] - Y[:-2])/2)*args.markersize
            #    pyplot.plot(X[1:-1], Y[1:-1], args.markerchar, alpha=args.alpha, markersize=Y_sizes)
            if 0 < len(X):# < 2:
                pyplot.plot(X, Y, args.markerchar, alpha=args.alpha, markersize=args.markersize)
                #pyplot.hexbin(X,Y, gridsize= (1, 1000), bins=1000)


        pyplot.xticks(range(1,len(x_labels)+1),x_labels)

    else:
        
        parser.print_help()
        parser.error("This type of plot needs to have -m and -n specified")
    

pyplot.show()
 

'''

