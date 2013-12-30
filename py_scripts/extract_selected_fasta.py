#!/usr/bin/env python
"""
    Script to extract fasta sequences with specified `terms` in description
    
    Args:
        fasta: fasta file to search
        terms: set of terms to search in fasta description
        
    Returns:
        fasta file containing only sequences containing one of the
        specified terms in description

    Created on Mon Dec 30 12:16:41 2013

    @author: John Stanton-Geddes
"""

#==============================================================================#

import argparse         # for parsing command line arguments
import os.path as osp   # for manipulating file names
from Bio import SeqIO   # for parsing sequence files

#==============================================================================#

#-----------------------------------------------------------------------
#
# Set up command line arguments -- these are just examples
# This will automatically generate a help message for you which
# will run if you either use '-h', '--help', or don't give the
# script the right number of positional arguments
#
# I also add a --doc option to display the __doc__ variable. To use this
# you have to put something in the place of the positional arguments,
# or the program just displays the help message and quits
#
#-----------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('--doc', action='store_true', default=False, # set this up as a true/false flag
                    help="Show documentation")
parser.add_argument('fasta') # input fasta file
parser.add_argument('terms') # text file containing search terms, one per line
args = parser.parse_args()

if args.doc:
    parser.print_help()
    print __doc__ + '\n'
    exit()

# Access the options
input_fasta = args.fasta
input_terms = args.terms

#--------------------------------------------------------------------

records = SeqIO.parse(input_fasta, "fasta")

#terms = ["Pogo"]
with open(input_terms) as t:
    terms = t.read().splitlines()

selected_records = []

for record in records:
    for term in terms:
        if term in record.description:
            # print record
            selected_records.append(record)

# create set of unique elements
unique_records = set(selected_records)

## write to file    
# create filename
output_prefix = osp.splitext(input_fasta)[0]
of = output_prefix + "_" + input_terms + ".fasta"
  
output_handle = open(of, "w")        
SeqIO.write(unique_records, output_handle, 'fasta')
output_handle.close()        
