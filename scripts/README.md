#Scripts

Useful scripts, general or tied to a specific program

##pairReads.py

USAGE: pairReads.py delim file1 file2 [matching field]

Sorts two fastq files and checks pairing. Output orphans to a separate file. 

##assign_contigs.py

Takes a file on fasta entries and assigns them as to either of two supplied reference data-bases.

Usable to classify entries e.g. as eucaryotic or bacterial.

##contig_sort_stat.py

Makes diagnostic stats and graphs based on contig assignment by _assign_contigs.py_

##fasta_filter.py

Filters a fasta file sequences on length.

##get_all_pattern.py

Filters fasta records for repeated patterns

##get_exact_matches.py

Find restriction enzyme patterns in fasta file

##get_inbetween_coord.py

Using lists of acsession numbers and sequence coordinates for those acsessions, downloads ther requested parts.

##patchy_matches.py

Calculates the entropy in blast hits

##prepend_to_rest.py

Simple script that adds the first argument to all consecutive arguments

##restrictions_hits_parser.py

Finds all occurencies of a pattern in a fasta file

##start_words_in_seq.py

Creates a frequency discionary of all N-length words at the beginning of sequences.
