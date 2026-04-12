#!/bin/bash

# Input folder and output file
input_folder="."
output_file="ScaledGenomicOutput.txt"

# Clear output file
> "$output_file"

# Loop through qmotif output files
for file in "$input_folder"/*_output.txt; do

  # Skip "terminal" files
  if [[ "$file" == *"terminal"* ]]; then
    echo "Skipping $file"
    continue
  fi

  # Extract sample name from BAM attribute
  filename=$(grep 'bam="' "$file" | sed 's|.*bam="[^/]\+/||; s|\..*||')

  # Extract scaled genomic count
  scaled_genomic=$(grep '<scaledGenomic' "$file" | sed 's|.*count="\([0-9]\+\)".*|\1|')

  # Save result
  echo "$filename \"$scaled_genomic\"" >> "$output_file"

done

echo "Processing completed. Results saved to $output_file."
