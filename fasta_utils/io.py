#!/usr/bin/env python3

import bzip2
import gzip
import lzma
import sys


LINE_WIDTH = 100


def openMaybeCompressed(path, mode='rt'):
    '''Opens a file that might be compressed in gzip, bzip2, or xz format

    Args:
        path - path to the fasta file
        mode - open in this mode
    '''

    handle = None
    if path.endswith('.bz2'):
        handle = bzip2.open(path, mode)
    elif path.endswith('.gz'):
        handle = gzip.open(path, mode)
    elif path.endswith('.xz'):
        handle = lzma.open(path, mode)
    else:
        handle = open(path, mode)
    return handle

def iterFasta(path):
    '''Iterates over the sequences of a fasta file.

    Args:
        path - path to the fasta file, for sys.stdin use None or '-'

    Returns:
        name, sequence tuple
    '''

    handle = sys.stdin
    if path and path != '-':
        handle = openMaybeCompressed(path)

    header = None
    seqLst = []
    for line in handle:
        line = line.strip()
        if not line:
            continue
        if line[0] == '>':
            if header is not None:
                seq = ''.join(seqLst)
                yield header, seq
            header = line[1:]
            seqLst.clear()
        elif header is not None:
            seqLst.append(line)
    if header is not None:
        seq = ''.join(seqLst)
        yield header, seq

    if path and path != '-':
        handle.close()

def loadFastaStrDict(path):
    '''Loads a set of fasta sequences as a dictionary of strings index by name

    Args:
        path - path to the fasta file, for sys.stdin use None or '-'

    Returns:
        A dictionary of sequences indexed by name
    '''

    sequences = {}
    for header, seq in iterFasta(path):
        sequences[header] = seq
    return sequences


def loadFastaStrList(path):
    '''Loads a set of fasta sequences as a list of sequences

    Args:
        path - path to the fasta file, for sys.stdin use None or '-'

    Returns:
        A list of sequences
    '''

    sequences = []
    for header, seq in iterFasta(path):
        sequences.append(seq)
    return sequences

def writeFastaSequence(handle, header, sequence, lineWidth=LINE_WIDTH):
    '''Writes one sequence out to a handle in fasta format

    Args:
        handle - output handle
        header - fasta header
        sequence - fasta sequence
        lineWidth - characters per line for the sequence, values of zero or
            less mean the whole sequence will be printed on a single line
    '''

    if lineWidth > 0:
        handle.write('>%s\n' % header)
        size = len(sequence)
        i = 0
        while i < size:
            handle.write('%s\n' % sequence[i:i + lineWidth])
            i += lineWidth
    else:
        handle.write('>%s\n%s\n' % (header, sequence))
