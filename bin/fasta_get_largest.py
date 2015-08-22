#!/usr/bin/env python3

import argparse
import heapq
import sys

import fasta_utils.io


def getArgs():
    parser = argparse.ArgumentParser(description='Get the largest sequence(s)')
    parser.add_argument('input',
                        nargs='*',
                        help='Input fasta file(s)')
    parser.add_argument('-n',
                        '--number',
                        metavar='NUM',
                        type=int,
                        default=1,
                        help='Number of sequences to keep')
    parser.add_argument('-m',
                        '--in-memory',
                        action='store_true',
                        help='Keep all the sequences in memory, potentially faster but uses more memory')
    parser.add_argument('-o',
                        '--output',
                        metavar='OUT',
                        help='Output file')
    args = parser.parse_args()
    return args

def allInMem(args):
    '''Stores all the sequences in memory and the sorts them find the largest.
    Runs in O(n) but memory usage can be high.
    '''

    inputs  = [None]
    out     = sys.stdout
    kept    = []
    count   = 0
    if args.input:
        inputs = args.input
    for path in inputs:
        for sequence in fasta_utils.io.iterFasta(path):
            kept.append(sequence)
    kept.sort(key=lambda x: len(x[1]))
    if len(kept) > args.number:
        kept = kept[-args.number:]
    kept.reverse()
    if args.output:
        out = fasta_utils.io.openMaybeCompressed(args.output, 'w')
    for sequence in kept:
        fasta_utils.io.writeFastaSequence(out, sequence[0], sequence[1])
    if args.output:
        out.close()

def notAllInMem(args):
    '''Only stores up to args.number sequences.
    Minimal memory usage, but O(n * log(n)) complexity.
    '''

    inputs  = [None]
    out     = sys.stdout
    kept    = []
    count   = 0
    if args.input:
        inputs = args.input
    for path in inputs:
        for sequence in fasta_utils.io.iterFasta(path):
            length = len(sequence)
            if count >= args.number:
                if length > kept[0][0]:
                    heapq.heapreplace(kept, (length, sequence))
            else:
                heapq.heappush(kept, (length, sequence))
                count += 1
    kept.sort(reverse=True)
    if args.output:
        out = fasta_utils.io.openMaybeCompressed(args.output, 'w')
    for length, sequence in kept:
        fasta_utils.io.writeFastaSequence(out, sequence[0], sequence[1])
    if args.output:
        out.close()

def main():
    args    = getArgs()
    if args.in_memory:
        allInMem(args)
    else:
        notAllInMem(args)

if __name__ == '__main__':
    main()
