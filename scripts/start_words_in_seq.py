#!/usr/bin/python

"""
This script will extract all initial N-sized words from sequences and
compile a hashed frequency dictionary.

A shorter species of genetic sequence (e.g. the adaptors used) is then
scored for each position for the frequency of that position's word in
the dicitonary.

"""

### DEPENDENCIES

import sys, os
from Bio import SeqIO
from argparse import ArgumentParser
from time import time

### Functions

def get_word_frequencies(word_length, search_file):

    freq_dict = {}

    file_endings = {'fa' : 'fasta', 'fq': 'fastq'}

    file_format = search_file.split(".")[-1]
    if file_format in file_endings.keys():
        file_format = file_endings[file_format]

    seq_so_far = 0
    seq_words = 0

    try:
        sequences = SeqIO.parse(search_file, file_format)
    except: 
        print "*** ERROR: Could not open input-file"
        return freq_dict

    for seq in sequences:

        try:
            freq_dict[str(seq.seq[:word_length])] += 1
        except KeyError:
            freq_dict[str(seq.seq[:word_length])] = 1
            seq_words += 1

        seq_so_far += 1

        ###BEGIN UNIT-TEST
        #print seq.seq[:word_length]
        #if seq_so_far > 50:
            #print freq_dict
            #sys.exit()
        ###END UNIT-TEST

        if seq_so_far % 50000 == 0:

            print "Searched " + str(seq_so_far) + " sequences"

    print "Frequencies dictionary completed, total " + \
        str(seq_words) + " words found in " +\
        str(seq_so_far) + " sequences."

    return freq_dict

def get_sequence_score(word_length, sequence, search_file=None, \
    freq_dict=None):

    score_list = []

    if search_file is None and freq_dict is None:
        return None

    if search_file is not None:
        freq_dict = get_word_frequencies(word_length, search_file)

    
    for pos in xrange(len(sequence)-word_length):
        #print sequence[pos:pos + word_length]
        try:
            score_list.append(freq_dict[sequence[pos:pos+word_length]])
        except KeyError:
            score_list.append(0)

    return score_list

### RUN BEHAVIOUR

if __name__ == "__main__":

    t = time()

    parser = ArgumentParser(description="The script ranks the positions in "\
        + "reference sequence according to the frequency of the N-length "\
        + "word (starting at that position) in a initiating sequences in a "\
        + "sequence file.")

    parser.add_argument('-l','--word-length', type=int, metavar="N", help="The \
        word-length investigated", dest="wordlength")

    parser.add_argument('-s', '--sequence', type=str, metavar="ATCG..", help= \
        "The sequency to score", dest="sequence")

    parser.add_argument('-i', '--input-file', type=str, metavar="PATH", help=\
        "The path to a file containing sequences to extract the intial word\
        for each sequence from", dest="input_file")

    parser.add_argument('-o', '--output-prefix', type=str, metavar="PATH", help=\
        "The path to where the graph should be saved", dest="output_file")

    args = parser.parse_args()

    if args.wordlength > 6:

        if raw_input('Note that memory usage increases drastically when \
            increasing word length. Are you sure you want to run it like\
            this? (Y/N)').upper() != 'Y':

            sys.exit()

    if args.wordlength is None or args.sequence is None or args.input_file \
        is None:

        parser.error('All arguments are except output_file are mandatory!')

    print "\n*** Compiling the data:"
    freq_dict = get_word_frequencies(args.wordlength, args.input_file)
    quality = get_sequence_score(args.wordlength, args.sequence, \
        freq_dict=freq_dict)

    tick_labels = []
    print
    for pos in xrange(len(args.sequence)-args.wordlength):
        
        print args.sequence[pos] + " " + str(quality[pos]) + ", ",
        tick_labels.append(args.sequence[pos: pos + args.wordlength])

    print

    if args.output_file is not None:

        import numpy as np
        import matplotlib
        matplotlib.use('Agg')

        from matplotlib import pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(111, title="QC-plot")
        ax.set_ylabel("freq")
        ax.plot(np.arange(len(quality)), np.asarray(quality))
        ax.set_xticks(np.arange(len(quality)))
        ax.set_xticklabels(tick_labels, rotation=270, fontsize='xx-small')
        ax.set_xlim(0, len(quality))

        try:
            plt.savefig(args.output_file +"_seq.png")
        except:
            print "***ERROR: Something went wrong saving the plot"
            sys.exit()
        print "\n*** Graph (1/2) saved as " + args.output_file + "_seq.png"

        sorted_keys = sorted(freq_dict)
        tick_labels=[]
        y_values = []

        for key in sorted_keys:

            tick_labels.append(key)
            y_values.append(freq_dict[key])
            
        fig = plt.figure()
        ax = fig.add_subplot(111, title="Freq distribution")
        ax.set_ylabel("freq")
        ax.plot(np.arange(len(y_values)), np.asarray(y_values))
        ax.set_xticks(np.arange(len(y_values)))
        ax.set_xticklabels(tick_labels, rotation=270, size='xx-small')
        ax.set_xlim(0, len(y_values))

        try:
            plt.savefig(args.output_file +"_allseq.png", dpi=300)
        except:
            print "***ERROR: Something went wrong saving the plot"
            sys.exit()

        print "\n*** Graph (2/2) saved as " + args.output_file + "_allseq.png"

    print "\nRun completed (" + str(time() - t) +" seconds).\n"

