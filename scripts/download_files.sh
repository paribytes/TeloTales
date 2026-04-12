#!/bin/bash

# Download WGS BAM files from Phase 3 of the 1000 Genomes Project
# Data source: https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/phase3/data/

set -e  # stop if any command fails

base_url="https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/phase3/data"

input_file="files_list.txt"

while IFS= read -r file_path; do
    wget -nc "${base_url}/${file_path}"
done < "${input_file}"
