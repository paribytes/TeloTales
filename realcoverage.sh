#!/bin/bash

# List all files ending with _coverage.txt and save them to a file called "output_coverage_filenames"
ls *_coverage.txt > output_coverage_filenames

# Loop through each coverage file
while read filename
do
    # Adds 'chr' to the beginning of every line in the file
    sed -i -e 's/^/chr/' $filename
    
    # Loop through each chromosome name from chrnames file
    while read chr
    do
        grep "^$chr[[:space:]]" "$filename"
        # Extract and tally telomere read counts for each chromosome, [[:space:]] was used to avoid chr10,...chr19 being counted in chr1 and chr20,21,22 being counted in chr2
        x=$(grep "^$chr[[:space:]]" "$filename" | awk '{sum+=$2} END {print sum}')

        # Append results to stage2coverage file
        echo "$filename $chr $x" >> stage2coverage
    done < chrnames
done < output_coverage_filenames

# Remove the '_coverage.txt' part from the filenames in the final file and save the results to "stage2coverage" file
sed -i -e 's/_stage2_coverage\.txt//g' stage2coverage


