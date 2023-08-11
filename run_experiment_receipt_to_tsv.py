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

    ids = {}
    for experiment in root.iter('EXPERIMENT'):
        alias = experiment.get('alias').split('exp_')[1]
        experiment_accession = experiment.get('accession')
        ids.setdefault(alias, []).append(experiment_accession)

    for run in root.iter('RUN'):
        alias = run.get('alias').split('run_')[1]
        run_accession = run.get('accession')
        ids.setdefault(alias, []).append(run_accession)

    ids_lines = [f'{k}\t{v[0]}\t{v[1]}' for k, v in ids.items()]

    # Write output TSV
    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(ids_lines)+'\n')


def parse_arguments():

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input-file', type=str, required=True,
                        dest='input_file',
                        help='Path to the input XML file with the data returned when the runs and experiments were registered.')

    parser.add_argument('-o', '--output-file', type=str, required=True,
                        dest='output_file',
                        help='Path to the output TSV file with the runs and experiments identifiers extracted from the input XML file.')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = parse_arguments()
    main(**vars(args))
