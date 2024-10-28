# TeloTales: Telomere Content Analysis Pipeline

This repository contains scripts and instructions for downloading BAM files from Phase 3 of the 1000 Genomes Project, analyzing telomeric content using qmotif, and saving output files with telomeric data. Each step in the pipeline is outlined below, along with requirements and execution instructions.

## Table of Contents
* Requirements
* File Descriptions
* Usage
* Detailed Steps

## Requirements
To run this pipeline, you'll need:
* **qmotif**: Download and install qmotif ([Documentation here](https://adamajava.readthedocs.io/en/latest/qmotif/qmotif_1_0/))
* **Java**: Required to run qmotif

## File Descriptions
  
## Usage

## Detailed Steps





Sequence to run the files:
1.) download_files.sh (requires: files_list.txt)
2.) hope2_bblah.py
3.) stage2.py (requires: log files generated by hope2_bblah.py)
4.) coverage.sh (requires: chrnames)
5.) totaltelomere.py (requires: stage2coverage)

1.	download_files.sh, along with files_list.txt will download the BAM and its corresponding BAI index file from NCBI’s 1000 Genomes Project server (https://www.ncbi.nlm.nih.gov/projects/faspftp/1000genomes/)
2.	Before running hope2_bblah.py (will rename the file later), make sure qmotif is installed and invoke java with the qmotif tar file. You’ll also need to set the path to the tool-qmotif and where your input files- BAM and BAI are. (more info on this-https://adamajava.readthedocs.io/en/latest/qmotif/qmotif_1_0/)
3.	stage2.py requires the log files generated by hope2_bblah.py (check what working directory you’re in before proceeding.) This script will give you the chromosome number and the final telomere motif counts for each chromosome after stage 2 -> this output will be stored in “{sequence_name}_stage2_coverage.txt file
4.	coverage.sh is to get a tally of telomere motifs for each chromosome. This script uses “chrnames” file, make sure they’re in the same folder. This script creates only one output file “stage2coverage” which has all the info on all the files you ran. 
5.	totaltelomere.py gives total telomere motif counts for the sequence across all chromosomes. This uses the “stage2coverage” file we got as an output in the previous step and generates a file named “total_telomere_motif_counts”


