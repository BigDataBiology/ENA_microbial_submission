#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script selects data from an input TSV file based on column names and
creates a new file with the selected data/coumns.
"""


import argparse

import pandas as pd


def main(input_file, output_file, columns, order, names):

    # Read input file
    data_table = pd.read_csv(input_file, sep='\t')

    # Select columns
    selected_data = data_table[columns]

    # Reorder columns if provided
    if order is not None:
        selected_data = selected_data[order]

    # Rename columns if provided
    if names is not None:
        current_columns = list(selected_data.columns)
        names_mapper = {current_columns[i]:n for i, n in enumerate(names)}
        selected_data = selected_data.rename(columns=names_mapper)

    # Save dataframe with selected data
    selected_data.to_csv(output_file, sep='\t', index=False)


def parse_arguments():

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input-file', type=str,
                        required=True, dest='input_file',
                        help='Path to the input TSV file.')

    parser.add_argument('-o', '--output-file', type=str,
                        required=True, dest='output_file',
                        help='Path to the output file created to store the selected data.')

    parser.add_argument('--columns', nargs='+', type=str,
                        required=True, dest='columns',
                        help='Names/identifiers of the columns to select.')

    parser.add_argument('--order', nargs='+', type=str,
                        dest='order',
                        help='Order of the names/identifiers of the columns in the output file.')

    parser.add_argument('--names', nargs='+', type=str,
                        dest='names',
                        help='New names/identifiers to attribute to the selected columns '
                             '(Must respect the order provided to `--order`).')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = parse_arguments()
    main(**vars(args))
