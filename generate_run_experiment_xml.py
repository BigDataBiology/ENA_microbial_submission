#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates a XML file to register runs and experiments in the ENA.
"""

import argparse
import hashlib
import os
import xml.etree.ElementTree as ET
from glob import glob

import pandas as pd


def md5(file):
    """Determine the MD5 checksum of a file."""

    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def create_submission_xml(output_directory):
    """Create the submission XML."""

    tree = ET.ElementTree("tree")
    # create parent tag
    parent_tag = ET.Element("SUBMISSION")
    # add ACTIONS tag
    actions_tag = ET.SubElement(parent_tag, "ACTIONS")
    # add ACTION tag
    action_tag = ET.SubElement(actions_tag, "ACTION")
    # add ADD tag
    add_tag = ET.SubElement(action_tag, "ADD")

    output_file = os.path.join(output_directory, "submission.xml")

    tree._setroot(parent_tag)
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)


def main(input_file, study, reads, output_prefix):
    """Create the XML file with the run and experiment data to submit."""

    # Read file with sample data
    data_table = pd.read_csv(input_file, sep="\t")

    # Create Experiments XML
    tree = ET.ElementTree("tree")

    # Create parent tag for experiment
    parent_tag = ET.Element("EXPERIMENT_SET")

    experiment_aliases = {}
    # Add tags for each sample
    for i in range(len(data_table)):
        current_sample = data_table.iloc[i]
        # Add EXPERIMENT tag
        experiment_tag = ET.SubElement(parent_tag, "EXPERIMENT")
        # Add alias attribute to EXPERIMENT tag
        experiment_alias = "exp_{0}".format(current_sample["alias"])
        experiment_aliases[current_sample["alias"]] = experiment_alias
        experiment_tag.set("alias", experiment_alias)
        experiment_tag.set("center_name", current_sample["center_name"])
        # Add TITLE tag
        title_tag = ET.SubElement(experiment_tag, "TITLE")
        title_tag.text = current_sample["title"]
        # Add STUDY_REF tag
        study_tag = ET.SubElement(experiment_tag, "STUDY_REF")
        study_tag.set("accession", study)
        # Add DESIGN tag
        design_tag = ET.SubElement(experiment_tag, "DESIGN")
        # Add DESIGN_DESCRIPTION tag
        design_description_tag = ET.SubElement(design_tag, "DESIGN_DESCRIPTION")
        # Add SAMPLE_DESCRIPTOR tag
        sample_descriptor_tag = ET.SubElement(design_tag, "SAMPLE_DESCRIPTOR")
        sample_descriptor_tag.set("accession", current_sample["ENA_accession"])
        # Add LIBRARY_DESCRIPTOR tag
        library_descriptor_tag = ET.SubElement(design_tag, "LIBRARY_DESCRIPTOR")
        # Add LIBRARY_NAME tag
        library_name_tag = ET.SubElement(library_descriptor_tag, "LIBRARY_NAME")
        # Add LIBRARY_STRATEGY tag
        library_strategy_tag = ET.SubElement(library_descriptor_tag, "LIBRARY_STRATEGY")
        library_strategy_tag.text = current_sample["library_strategy"]
        # Add LIBRARY_SOURCE tag
        library_source_tag = ET.SubElement(library_descriptor_tag, "LIBRARY_SOURCE")
        library_source_tag.text = current_sample["library_source"]
        # Add LIBRARY_SELECTION tag
        library_selection_tag = ET.SubElement(
            library_descriptor_tag, "LIBRARY_SELECTION"
        )
        library_selection_tag.text = current_sample["library_selection"]
        # Add LIBRARY_LAYOUT tag
        library_layout_tag = ET.SubElement(library_descriptor_tag, "LIBRARY_LAYOUT")
        # Add PAIRED tag
        # paired_layout_tag = ET.SubElement(library_layout_tag, current_sample['library_layout'].upper())
        # paired_layout_tag.set('NOMINAL_LENGTH', str(current_sample['nominal_length']))
        # Add PLATFORM tag
        platform_tag = ET.SubElement(experiment_tag, "PLATFORM")
        platform_info_tag = ET.SubElement(
            platform_tag, current_sample["platform"].upper()
        )
        # Add INSTRUMENT_MODEL tag
        instrument_tag = ET.SubElement(platform_info_tag, "INSTRUMENT_MODEL")
        instrument_tag.text = current_sample["instrument_model"]
        # Add EXPERIMENT_ATTRIBUTES tag
        experiment_attributes_tag = ET.SubElement(
            experiment_tag, "EXPERIMENT_ATTRIBUTES"
        )

    # Create XML with data to submit Experiments
    tree._setroot(parent_tag)
    output_file = "{0}_experiments.xml".format(output_prefix)
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)

    # Create Runs XML
    run_tree = ET.ElementTree("tree")

    # Create parent tag for experiment
    parent_tag = ET.Element("RUN_SET")

    # Get list of Reads files
    reads_files = glob(f"{reads}**/*.gz", recursive=True)
    reads_dict = {}
    for file in reads_files:
        sample_id = file.split(".pair.")[0]
        reads_dict.setdefault(sample_id, []).append(file)

    # Determine MD5 checksum
    files_md5 = {}
    for file in reads_files:
        files_md5[file] = md5(os.path.join(reads, file))

    # Add tags for each sample
    for i in range(len(data_table)):
        current_sample = data_table.iloc[i]
        # Add EXPERIMENT tag
        run_tag = ET.SubElement(parent_tag, "RUN")
        run_alias = "run_{0}".format(current_sample["alias"])
        run_tag.set("alias", run_alias)
        run_tag.set("center_name", current_sample["center_name"])
        # Add EXPERIMENT_REF tag
        experiment_ref_tag = ET.SubElement(run_tag, "EXPERIMENT_REF")
        experiment_ref_tag.set("refname", experiment_aliases[current_sample["alias"]])
        # Add DATA_BLOCK tag
        data_block_tag = ET.SubElement(run_tag, "DATA_BLOCK")
        # Add FILES tag
        files_tag = ET.SubElement(data_block_tag, "FILES")
        # Add FILE tag for R1
        file_r1_tag = ET.SubElement(files_tag, "FILE")
        r1_file = [
            file
            for file in reads_dict[current_sample["alias"]]
            if file.endswith("1.fq.gz")
        ][0]
        file_r1_tag.set("checksum", files_md5[r1_file])
        file_r1_tag.set("checksum_method", "MD5")
        file_r1_tag.set("filetype", "fastq")
        file_r1_tag.set("filename", r1_file)
        # Add FILE tag for R2
        file_r2_tag = ET.SubElement(files_tag, "FILE")
        r2_file = [
            file
            for file in reads_dict[current_sample["alias"]]
            if file.endswith("2.fq.gz")
        ][0]
        file_r2_tag.set("checksum", files_md5[r2_file])
        file_r2_tag.set("checksum_method", "MD5")
        file_r2_tag.set("filetype", "fastq")
        file_r2_tag.set("filename", r2_file)

    # Create XML with data to submit Experiments
    run_tree._setroot(parent_tag)
    output_file = "{0}_runs.xml".format(output_prefix)
    run_tree.write(output_file, encoding="UTF-8", xml_declaration=True)

    # Create the submission XML
    output_directory = os.path.dirname(output_file)
    create_submission_xml(output_directory)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-i",
        "--input-file",
        type=str,
        required=True,
        dest="input_file",
        help="Path to the input TSV file with the metadata that should be included in the XML.",
    )

    parser.add_argument(
        "--study",
        type=str,
        required=True,
        dest="study",
        help="Identifier of the Study the runs and experiments will be linked to.",
    )

    parser.add_argument(
        "--reads",
        type=str,
        required=True,
        dest="reads",
        help="Path to the directory that contains the sequencing reads files (fastq.gz).",
    )

    parser.add_argument(
        "-o",
        "--output-prefix",
        type=str,
        required=False,
        dest="output_prefix",
        help="Prefix added to the XML file basename.",
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_arguments()
    main(**vars(args))
