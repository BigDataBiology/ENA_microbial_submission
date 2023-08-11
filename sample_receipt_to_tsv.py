#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script extracts the sample identifiers contained in the XML data
returned when a collection of samples are registered in the ENA.
"""


import argparse
import xml.etree.cElementTree as et


def main(input_file, output_file):

    tree = et.parse(input_file)
    root = tree.getroot()

    ids = []
    for sample in root.iter('SAMPLE'):
        alias = sample.get('alias')
        ena_accession = sample.get('accession')
        biosample = sample[0].get('accession')
        ids.append(f'{alias}\t{biosample}\t{ena_accession}')

    # Write output TSV
    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(ids)+'\n')


def parse_arguments():

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input-file', type=str, required=True,
                        dest='input_file',
                        help='Path to the input XML file with the data returned when the samples were registered.')

    parser.add_argument('-o', '--output-file', type=str, required=True,
                        dest='output_file',
                        help='Path to the output TSV file with the sample identifiers extracted from the input XML file.')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = parse_arguments()
    main(**vars(args))
