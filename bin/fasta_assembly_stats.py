#!/usr/bin/env python3

import argparse
import collections
import random
import sys

import fasta_utils.io


LETTERS = ('A', 'C', 'G', 'T', 'N')

def getArgs():
    parser = argparse.ArgumentParser(description='Compute basic assembly stats')
    parser.add_argument('input',
                        nargs='*',
                        help='Input fasta file(s)')
    parser.add_argument('-o',
                        '--output',
                        metavar='OUT',
                        help='Output file')
    args = parser.parse_args()
    return args

def main():
    args    = getArgs()
    inputs  = [None]
    sizes   = []
    n       = 0
    letters = collections.defaultdict(int)
    if args.input:
        inputs = args.input
    # Reservoir sampling algorithm
    for path in inputs:
        for header, sequence in fasta_utils.io.iterFasta(path):
            sequence = sequence.upper()
            n       += 1
            sizes.append(len(sequence))
            for letter in LETTERS:
                letters[letter] += sequence.count(letter)
    sizes.sort()
    median = sizes[n // 2]
    mean   = sum(sizes) / n
    cumsum = sizes[:1]
    for i in range(1, n):
        cumsum.append(cumsum[i - 1] + sizes[i])
    total  = cumsum[-1]
    for i in range(n):
        if cumsum[i] * 2 >= total:
            n50 = sizes[i]
            break
    letterComposition = []
    for letter in LETTERS:
        letterNum = letters[letter]
        letterComposition.append('%s %d (%.2f%%)' % (letter, letterNum, 100 * letterNum / total))
    letterComposition = ', '.join(letterComposition)
    # Write output
    out = sys.stdout
    if args.output:
        out = fasta_utils.io.openMaybeCompressed(args.output, 'w')
    out.write('Total    : %d\n' % total)
    out.write('Number   : %d\n' % n)
    out.write('Smallest : %d\n' % min(sizes))
    out.write('Largest  : %d\n' % max(sizes))
    out.write('Mean     : %d\n' % mean)
    out.write('Median   : %d\n' % median)
    out.write('N50      : %d\n' % n50)
    out.write('Letters  : %s\n' % letterComposition)
    if args.output:
        out.close()

if __name__ == '__main__':
    main()
