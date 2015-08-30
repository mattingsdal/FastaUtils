#!/usr/bin/env python3

import argparse
import sys

import fasta_utils.io


def getArgs():
    parser = argparse.ArgumentParser(description='Gets the list of sequence sizes')
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
    out     = sys.stdout
    if args.output:
        out = fasta_utils.io.openMaybeCompressed(args.output, 'w')
    if args.input:
        inputs = args.input
    for path in inputs:
        for header, sequence in fasta_utils.io.iterFasta(path):
            length = len(sequence)
            out.write('%d\n' % length)
    if args.output:
        out.close()

if __name__ == '__main__':
    main()
