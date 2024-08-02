# Submission of microbial sample data to the European Nucleotide Archive (ENA)

We suggest you read the [General Guide On ENA Data Submission](https://ena-docs.readthedocs.io/en/latest/submit/general-guide.html). This repo contains scripts and instructions to submit raw reads programmatically. The only step performed interactively is the [Study Registration](https://ena-docs.readthedocs.io/en/latest/submit/study.html). You need to have a Webin submission account to be able to submit data to the ENA (information about creating an account [here](https://ena-docs.readthedocs.io/en/latest/submit/general-guide/registration.html#register-a-submission-account)).

## Register Study

Review the [Register a Study Interactively](https://ena-docs.readthedocs.io/en/latest/submit/study/interactive.html) section. We find it easier to register a new Study interactively, especially when the raw reads we want to submit will become associated with a single Study, but you can find instructions to do this programmatically on the [Register a Study Programmatically](https://ena-docs.readthedocs.io/en/latest/submit/study/programmatic.html) section. We suggest you define a release date well beyond the present date to avoid making the Study publicly available when you still need to edit it. You can change the release date when everything is ready. Do not forget to save the BioProject (begins with `PRJEB`) and Study (begins with `ER`) accession numbers.

## Register Samples

The next step is to register your samples. You can find information about this step on the [How to Register Samples](https://ena-docs.readthedocs.io/en/latest/submit/samples.html) and [Register Samples Programmatically](https://ena-docs.readthedocs.io/en/latest/submit/samples/programmatic.html) sections. We will use the ERC000028 checklist (ENA prokaryotic pathogen minimal sample checklist, available [here](https://www.ebi.ac.uk/ena/browser/view/ERC000028)). We will be constructing the XML based on the fields in the checklist (we will not modify the checklist file for submission). This repo includes a TSV file, `test_sample_metadata.tsv`, with example metadata necessary to create the XML file to register samples in the ENA. You can leave the `center_name` field empty. The centre name is automatically assigned from submission account details, and any value that you include in the metadata will be ignored (more information about this [here](https://ena-docs.readthedocs.io/en/latest/submit/general-guide/programmatic.html#identifying-submitters)). To create the XML file based on your sample metadata, run the `ena_samples_xml.py` script. Adapt the following command:

```
python generate_sample_xml.py -i test_sample_metadata.tsv -o sample.xml -c ERC000028
```

This will create an XML file with the data to register the samples and the accompanying submission XML file, `submission.xml`.
To submit the XML files and register your Samples, you can run the following command:

```
curl -u username:password -F "SUBMISSION=@submission.xml" -F "SAMPLE=@sample.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
```

Remember to save the response to a file (copy what is printed to the terminal or pipe the result to a file). If you get `curl: (26) Failed to open/read local data from file/application`, the name of the submission or samples XML might be incorrect. Check that and try again. More information is available [here](https://ena-docs.readthedocs.io/en/latest/submit/samples/programmatic.html#submit-the-xmls-using-curl). Please provide your Webin submission account credentials using the `username` and `password` (do not add single or double quotes to the username or password). You should test your submissions before submitting the data to the production service. Find more information about using the Test service in the [Test and production services](https://ena-docs.readthedocs.io/en/latest/submit/samples/programmatic.html#test-and-production-services) section. If you need to update the metadata for samples that have already been registered, simply edit the data in the XML file used to register the samples and change the `<ADD/>` tag in the submission XML to `<MODIFY/>` (example [here](https://ena-docs.readthedocs.io/en/latest/update/metadata/programmatic-sample.html). The `sample_receipt_to_tsv.py` script creates a TSV file with the correspondence between the sample Alias, BioSample and alternative accession number (starts with `ERS`). This TSV file can be the starting point to create the metadata file necessary to generate the XML to register Runs and Experiments.

## Prepare and Upload Read Files

The FASTQ files must be compressed using gzip or bzip2 (check the section about [Preparing A File For Upload](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/preparation.html#preparing-a-file-for-upload)). The `generate_run_experiment_xml.py` script determines the checksums and creates the XML file to register your Runs and Experiments. In this step, you only need to make sure that your files are compressed and that the filenames are in the format `<SAMPLE_ALIAS>_{1,2}.fastq.gz` (The `SAMPLE_ALIAS` is the value used as `alias` in the TSV file with the sample metadata).
To upload read files:

1. Open a terminal and type `lftp webin2.ebi.ac.uk -u Webin-xxxxx`, filling in your Webin username (must have `lftp` installed).
2. Enter your password when prompted.
3. Type `ls` to check the content of your dropbox.
4. Upload files using the `mput <filename>` command.
5. Use the `bye` command to exit the FTP client.

If the `ls` command gets stuck at `Making data connection...`, try to connect to the server through `ftp` with the following command: `ftp -i Webin-xxxxx@webin2.ebi.ac.uk`.

This will upload the read files to your private Webin file upload area using FTP. After registering the Runs and Experiments, the server automatically links the files to the Run and Experiment records.

## Register Runs and Experiments

You must create a TSV file with the data necessary to register the Runs and Experiments. This repo includes a TSV file, `test_run_experiment_metadata.tsv`, with example metadata required to create the XML file to register Runs and Experiments in the ENA. To create the XML file to register your Runs and Experiments, you should run the `generate_run_experiment_xml.py` script. Adapt the following command:

```
python generate_run_experiment_xml.py -i test_run_experiment_metadata.tsv -o studyID --study studyID --reads readsDirectory
```

The `studyID` is the BioProject accession number attributed when registering the Study.
To submit the XML files and register your Runs and Experiments, you can run the following command:

```
curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@experiment.xml" -F "RUN=@run.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
```

Remember to save the response to a file. The `run_experiment_receipt_to_tsv.py` script can create a TSV file with the correspondence between the sample Alias, Run accession and Experiment accession.
The server should link the read files uploaded to the Runs and Experiments that were just registered. Each Run entry should have associated read files with an `Archive status` of `File submitted`, which will change to `File archived` when the files have been moved from your private Webin file upload area to the permanent storage area (this will happen after the Study has become public). Remember to change the release date of the Study to make it publicly available.
