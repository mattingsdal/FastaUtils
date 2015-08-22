#!/usr/bin/env python3

import argparse
import re
import sys

import fasta_utils.io


def getArgs():
    parser = argparse.ArgumentParser(description='Finds sequences matching a pattern')
    parser.add_argument('pattern',
                        help='Search pattern')
    parser.add_argument('input',
                        nargs='*',
                        help='Input fasta file(s)')
    parser.add_argument('-c',
                        '--count',
                        action='store_true',
                        help='Print count of matching sequences')
    parser.add_argument('-s',
                        '--search-sequence',
                        action='store_true',
                        help='Search sequences for pattern instead of header')
    parser.add_argument('-m',
                        '--max-count',
                        metavar='NUM',
                        type=int,
                        default=0,
                        help='Stop after NUM matching sequences')
    args = parser.parse_args()
    return args

def main():
    args   = getArgs()
    inputs = [None]
    regexp = re.compile(args.pattern)
    count  = 0
    maxed  = False
    if args.input:
        inputs = args.input
    for path in inputs:
        for header, sequence in fasta_utils.io.iterFasta(path):
            matched = False
            if args.search_sequence:
                if regexp.match(sequence):
                    matched = True
            else:
                if regexp.match(header):
                    matched = True
            if matched:
                count += 1
                if not args.count:
                    fasta_utils.io.writeFastaSequence(sys.stdout, header, sequence)
                if args.count > 0 and count == args.count:
                    maxed = True
                    break
        if maxed:
            break
    if args.count:
        print(count)

if __name__ == '__main__':
    main()
