import os
import subprocess

# Get a list of all files in the current directory
files = os.listdir(".")

# Loop through each file in the directory
for file in files:
    # Checking if the file name ends with '_log.txt'
    if file.endswith("_log.txt"):
        # Extracting just the sequence name from the file
        sequence_name = file.replace("_log.txt", "")
        
        # Define the grep command using the sequence name
        #This extracts the chromosome number and the final telomere motif counts each chromosome has after stage2
        grep_command = f"grep 'GENOMIC' {file} | awk '{{split($6, arr, \":\"); print arr[1]\"\\t\"$18}}' | sed 's/,/\t/g' > {sequence_name}_stage2_coverage.txt"
        
        # Execute the grep command
        subprocess.run(grep_command, shell=True)




