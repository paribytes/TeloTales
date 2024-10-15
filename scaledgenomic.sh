#!/bin/bash

# Define input folder and output file
input_folder="/Users/pshah4374/Documents/FinalChapter1/Telomere_1kGP_qMotif_Files_PHASE3_Backup2"  # Replace with your folder path
output_file="ScaledGenomicOutput.txt"


# Clear the output file if it exists
> "$output_file"

# Loop through *_output.txt files but exclude those with "terminal" in the name
for file in "$input_folder"/*_output.txt; do
  # Skip files with 'terminal' in their name
  if [[ "$file" == *"terminal"* ]]; then
    echo "Skipping $file"
    continue
  fi

  # Extract the filename from the 'bam' attribute
  filename=$(grep 'bam="' "$file" | sed 's|.*bam="[^/]\+/||;s|\..*||')

  # Extract the scaledGenomic count
  scaled_genomic=$(grep '<scaledGenomic' "$file" | sed 's|.*count="\([0-9]\+\)".*|\1|')

  # Write the result to the output file
  echo "$filename \"$scaled_genomic\"" >> "$output_file"
done

echo "Processing completed. Results saved to $output_file."