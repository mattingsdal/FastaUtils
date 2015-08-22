#!/usr/bin/env python3

import argparse
import random
import re
import sys

import fasta_utils.io


def getArgs():
    parser = argparse.ArgumentParser(description='Filter sequences by size')
    parser.add_argument('input',
                        nargs='*',
                        help='Input fasta file(s)')
    parser.add_argument('-s',
                        '--smaller-than',
                        metavar='SIZE',
                        type=int,
                        help='Only get sequenes strictly smaller than SIZE')
    parser.add_argument('-l',
                        '--larger-than',
                        metavar='SIZE',
                        type=int,
                        help='Only get sequenes strictly larger than SIZE')
    parser.add_argument('-o',
                        '--output',
                        metavar='OUT',
                        help='Output file')
    args = parser.parse_args()
    return args

def main():
    args    = getArgs()
    inputs  = [None]
    minSize = args.smaller_than
    maxSize = args.lager_than
    out     = sys.stdout
    if args.output:
        out = openMaybeCompressed(args.output, 'w')
    if not args.seed is None:
        random.seed(args.seed)
    if args.input:
        inputs = args.input
    for path in inputs:
        for header, sequence in fasta_utils.io.iterFasta(path):
            length = len(sequence)
            keep   = True
            if not minSize is None and length < minSize:
                keep = False
            if not maxSize is None and length > maxSize:
                keep = False
            if keep:
                fasta_utils.io.writeFastaSequence(out, header, sequence)
    if args.output:
        out.close()

if __name__ == '__main__':
    main()
