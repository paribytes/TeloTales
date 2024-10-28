#!/bin/bash

#This script (together with the "files_list.txt" file) will download WGS BAM files from Phase 3 of the 1000 Genomes Project by utilizing NCBI's site (https://www.ncbi.nlm.nih.gov/projects/faspftp/1000genomes/)

#Since the base URL is the same for all files, I made the base URL a bash variable. All the file paths are stored in the "files_list.txt" file.

base_url="https://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/phase3/data"

#ensuring that the entire line is read as a whole so the link can work
#file_path variable stores the content of each line from files_list.txt file
#wget is used to download files from the web and then concatenate the entire file path

while IFS= read -r file_path; do
    wget "${base_url}/${file_path}"
done < files_list.txt
