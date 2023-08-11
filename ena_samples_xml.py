#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates a XML file to register a list of samples in the ENA.
"""


import os
import argparse
import xml.etree.ElementTree as ET

import pandas as pd


def create_submission_xml(output_directory):
    """Create the submission XML."""

    tree = ET.ElementTree('tree')
    # Create parent tag
    parent_tag = ET.Element('SUBMISSION')
    # Add ACTIONS tag
    actions_tag = ET.SubElement(parent_tag, 'ACTIONS')
    # Add ACTION tag
    action_tag = ET.SubElement(actions_tag, 'ACTION')
    # Add ADD tag
    add_tag = ET.SubElement(action_tag, 'ADD')

    output_file = os.path.join(output_directory, 'submission.xml')

    tree._setroot(parent_tag)
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)


def main(input_file, output_file, checklist):
    """Create the XML file with the sample data to submit."""

    # Read input file with sample metadata
    data_table = pd.read_csv(input_file, sep='\t')

    # Get headers to add as sample attributes
    attributes = list(data_table.columns)
    attributes = [a
                  for a in attributes
                  if a not in ['alias', 'title', 'taxon_id', 'center_name']]

    tree = ET.ElementTree('tree')

    # Create parent tag
    parent_tag = ET.Element('SAMPLE_SET')

    # Add tags for each sample
    for i in range(len(data_table)):
        current_sample = data_table.iloc[i]
        # Add SAMPLE tag
        sample_tag = ET.SubElement(parent_tag, 'SAMPLE')
        # Add alias attribute to SAMPLE tag
        sample_tag.set('alias', current_sample['alias'])
        # Add center_name attribute to SAMPLE tag
        sample_tag.set('center_name', current_sample['center_name'])
        # Add TITLE tag
        title_tag = ET.SubElement(sample_tag, 'TITLE')
        title_tag.text = current_sample['title']
        # Add SAMPLE_NAME tag
        sample_name_tag = ET.SubElement(sample_tag, 'SAMPLE_NAME')
        # Add TAXON_ID tag
        taxonid_tag = ET.SubElement(sample_name_tag, 'TAXON_ID')
        taxonid_tag.text = str(current_sample['taxon_id'])

        # Create SAMPLE_ATTRIBUTES tags and add each attribute value
        sample_attributes_tag = ET.SubElement(sample_tag, 'SAMPLE_ATTRIBUTES')
        for a in attributes:
            current_attribute = a
            current_value = current_sample[current_attribute]
            current_attribute_tag = ET.SubElement(sample_attributes_tag, 'SAMPLE_ATTRIBUTE')
            # Add TAG tag
            current_tag_tag = ET.SubElement(current_attribute_tag, 'TAG')
            current_tag_tag.text = current_attribute.lower()
            # Add VALUE tag
            current_value_tag = ET.SubElement(current_attribute_tag, 'VALUE')
            current_value_tag.text = str(current_value)

        # Add ENA checklist identifier to each sample
        if checklist is not None:
            checklist_attribute_tag = ET.SubElement(sample_attributes_tag, 'SAMPLE_ATTRIBUTE')
            # Add TAG tag
            checklist_attribute_tag_tag = ET.SubElement(checklist_attribute_tag, 'TAG')
            checklist_attribute_tag_tag.text = 'ENA-CHECKLIST'
            # Add VALUE tag
            checklist_attribute_tag_value = ET.SubElement(checklist_attribute_tag, 'VALUE')
            checklist_attribute_tag_value.text = checklist

    tree._setroot(parent_tag)
    # Write XML file with sample data
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)

    # Write the submission XML
    output_directory = os.path.dirname(output_file)
    create_submission_xml(output_directory)


def parse_arguments():

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input-file', type=str, required=True,
                        dest='input_file',
                        help='Path to the input TSV file with the metadata that should be included in the XML.')

    parser.add_argument('-o', '--output-file', type=str, required=True,
                        dest='output_file',
                        help='Path to the output XML file (please include the .xml extension.)')

    parser.add_argument('-c', '--checklist', type=str, required=True,
                        dest='checklist',
                        help='Identifier of the checklist to use (e.g. ERC000028).')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = parse_arguments()
    main(**vars(args))
