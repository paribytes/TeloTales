#!/bin/bash

# List all coverage files
ls *_coverage.txt > output_coverage_filenames

# Initialize output file
> stage2coverage

# Loop through each coverage file
while read -r filename
do
    # Add 'chr' prefix to each line 
    sed -i -e 's/^/chr/' "$filename"

    # Loop through chromosome list
    while read -r chr
    do
        # Sum telomere read counts for each chromosome 
        # [[:space:]] was used to avoid chr10,..,chr19 being counted in chr1 and chr20,21,22 being counted in chr2
        x=$(grep "^$chr[[:space:]]" "$filename" | awk '{sum+=$2} END {print sum}')

        # Append results
        echo "$filename $chr $x" >> stage2coverage

    done < chrnames.txt

done < output_coverage_filenames

# Clean filenames in final output
sed -i -e 's/_stage2_coverage\.txt//g' stage2coverage
