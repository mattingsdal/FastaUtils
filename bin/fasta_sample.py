#!/usr/bin/env python3

import argparse
import random
import re
import sys

import fasta_utils.io


def getArgs():
    parser = argparse.ArgumentParser(description='Randomly sample sequences')
    parser.add_argument('input',
                        nargs='*',
                        help='Input fasta file(s)')
    parser.add_argument('-n',
                        '--number',
                        metavar='NUM',
                        type=int,
                        default=1,
                        help='Number of sequences to sample')
    parser.add_argument('-o',
                        '--output',
                        metavar='OUT',
                        help='Output file')
    parser.add_argument('-s',
                        '--seed',
                        metavar='SEED',
                        type=int,
                        help='Seed for the random number generator')
    args = parser.parse_args()
    return args

def main():
    args    = getArgs()
    inputs  = [None]
    sampled = []
    targetn = args.number
    i       = 0
    if not args.seed is None:
        random.seed(args.seed)
    if args.input:
        inputs = args.input
    # Reservoir sampling algorithm
    for path in inputs:
        for sequence in fasta_utils.io.iterFasta(path):
            i += 1
            if i <= targetn:
                sampled.append(sequence)
            elif random.random() < targetn / i:
                    which = random.randint(1, targetn) - 1
                    sampled[which] = sequence
    # Write output
    out = sys.stdout
    if args.output:
        out = openMaybeCompressed(args.output, 'w')
    for header, sequence in sampled:
        fasta_utils.io.writeFastaSequence(out, header, sequence)
    if args.output:
        out.close()

if __name__ == '__main__':
    main()
