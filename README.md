# Submission of microbial sample data to the European Nucleotide Archive (ENA)

We suggest that you start by reading the General Guide On ENA Data Submission https://ena-docs.readthedocs.io/en/latest/submit/general-guide.html. This repo contains scripts and instructions to submit raw reads programmatically. The only step that is performed interactively is the Study Registration. You need to have Webin submission account to be able to submit data to the ENA (informationa bout creating an account here https://ena-docs.readthedocs.io/en/latest/submit/general-guide/registration.html#register-a-submission-account)


Start by registering a Study. You can find instructions about this step here https://ena-docs.readthedocs.io/en/latest/submit/study.html and here https://ena-docs.readthedocs.io/en/latest/submit/study/interactive.html. We find it easier to register a new Study interactively, especially when the raw reads we want to submit will become associated to a single Study, but you can find instructions to do this programatically here https://ena-docs.readthedocs.io/en/latest/submit/study/programmatic.html.

The next step is to register samples. You can find information about this step here https://ena-docs.readthedocs.io/en/latest/submit/samples.html and here https://ena-docs.readthedocs.io/en/latest/submit/samples/programmatic.html. We will use the ERC000028 checklist (ENA prokaryotic pathogen minimal sample checklist, available here https://www.ebi.ac.uk/ena/browser/view/ERC000028). We will be constructing the XML based on the fields in the checklist (we will not modify the checklist file for submission). This repo includes a TSV file, test_metadata.tsv, with example metadata necessary to register samples in the ENA. To create the XML file to register your samples you should run the following command:

python ena_samples_xml.py -i test_sample_metadata.tsv -o sample.xml -c ERC000028

This will create a XML file with the data to register the samples and the accompanying submission XML file, submission.xml.
To submit the XML files and register your samples, you can run the following command:

curl -u username:password -F "SUBMISSION=@submission.xml" -F "SAMPLE=@sample.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"

This information is also availabel here https://ena-docs.readthedocs.io/en/latest/submit/samples/programmatic.html#submit-the-xmls-using-curl. Please provide your Webin submission account credentials using the username and password. You should test your submissions before submitting the data to the production service (more information here https://ena-docs.readthedocs.io/en/latest/submit/samples/programmatic.html#test-and-production-services).

To upload read files:

1. Open a terminal and type lftp webin2.ebi.ac.uk -u Webin-xxxxx, filling in your Webin username (must have lftp installed).
2. Enter your password when prompted.
3. Type ls command to check the content of your drop box.
4. Use mput <filename> command to upload files.
5. Use bye command to exit the ftp client.

Register Runs and Experiments:

You should prepare the FASTQ files for upload. FASTQ files must be compressed before upload (with gzip or bzip2, more information here https://ena-docs.readthedocs.io/en/latest/submit/fileprep/preparation.html#preparing-a-file-for-upload).
You also need to create a TSV file with the data necessary to register the runs and experiments. To create the XML files to register the Runs and Experiments, run the following command:

python ena_reads.xml.py -i test_run_experiment_metadata.tsv -o datasetID --study studyID --reads readsDir

curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@experiment.xml" -F "RUN=@run.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
