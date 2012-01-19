#!/usr/bin/python

"""
FINDS ALL OCCURANCES OF A PATTERN IN A FASTA FILE

"""

from argparse import ArgumentParser
from matplotlib import pyplot
import numpy as np

parser = ArgumentParser(description='This script will eventually give you all restriction enzyme hits')
parser.add_argument("-i", "--input-file", dest="inputfile", help="Sequence input file to cut in.", metavar="FILE")
parser.add_argument("-r", "--restriction-sequence", dest="patterns", help="Comma-separated list of restriction enzyme patterns", metavar="PATTERN(S)")
parser.add_argument("-m", "--minimum-distance", dest="low", help="The lower distance threshold for reporting", metavar="N")
parser.add_argument("-n", "--maximum-distance", dest="high", help="The lower distance threshold for reporting", metavar="N")
parser.add_argument("-p", "--plot", dest="plot", help="The type of plot you want to see: 'dist' (default), distance vs frequency plot. 'cont' gives a contig positions plot", metavar="PLOT", default="dist")
parser.add_argument("-a", "--alpha", dest="alpha", type=float, help="Set alpha value (0-1) for each marking on cont-plot. Default: 0.1", default=0.1, metavar="0.NN")

args = parser.parse_args()

try:
    fs = open(args.inputfile)
except:
    parser.print_help()
    parser.error("Couldn't locate inputfile")

common_re = {'EcoR1': 'GAATTC'}

try:
    patterns = args.patterns.split(",")
except:
    parser.print_help()
    parser.error("Bad restriction patterns!")

for i, p in enumerate(patterns):
    if p in common_re.keys():
        patterns[i] = common_re[p]

results_dict = None
pos_dict = None
contig_dict = None

for line in fs.readlines():
    if line[0] != "@":
        if results_dict == None:        
            results_dict = eval(line)
        elif pos_dict == None:
            pos_dict = eval(line)
        elif contig_dict == None:
            contig_dict = eval(line)
        else:
            break

fs.close()

pyplot.clf()

if args.plot == "dist":

    X = np.asarray(map(int, results_dict[patterns[0]]))


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
    Y = np.asarray(results_dict[patterns[0]].values())
    Y_filtered = Y[X_filter]
    pyplot.plot(X_filtered, Y_filtered, 'r.')

elif args.plot == "cont":
    if args.low != None and args.high != None:
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
            pyplot.plot(X, Y, 'r.', alpha=args.alpha)

        pyplot.xticks(range(1,len(x_labels)+1),x_labels)

    else:
        
        parser.print_help()
        parser.error("This type of plot needs to have -m and -n specified")
    

pyplot.show()
 


