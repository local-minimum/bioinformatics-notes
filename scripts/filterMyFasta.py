#!/usr/bin/env python
"""Filters a fasta file based on partial headers in another file.

TODO:
    * Check if dataFile exists nicely
    * Check if filterFile exists nicely
    * Ask if overwrite if outputFile exist (maybe add allways overwrite)
    * Allow for other versions of filtering criteria

Author: Martin Zackrisson
"""
import sys

if len(sys.argv) < 4:
    print("Usage: {0} dataFilePath filterFilePath outputFilePath".format(sys.argv[0]))
    sys.exit(0)
else:
    dataFile = sys.argv[1]
    filterFile = sys.argv[2]
    outputFile = sys.argv[3]

splitChar = " "
outputNext = False

with open(filterFile, 'r') as fhFilter:
    myFilter = set()
    for line in fhFilter:
	for linePart in line.split("\r"):
            myFilter.add(linePart.split(splitChar, 1)[0])

with open(dataFile, 'r') as fhDataFile:

    with open(outputFile, 'w') as fhOutput:

        for line in fhDataFile:

            if outputNext:
                fhOutput.write(line)
                outputNext = False
            elif line.split(splitChar, 1)[0] in myFilter:
                fhOutput.write(line)
                outputNext = True
