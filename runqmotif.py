import subprocess

#set the path to qmotif and your working directory
#for more info on qmotif, visit this: https://adamajava.readthedocs.io/en/latest/qmotif/qmotif_1_0/

#export PATH=$PATH:/home/priyanshi/Documents/telomerework
#export PATH=$PATH:/home/priyanshi/Documents/telomerework/qmotif
#export PATH=$PATH:/home/priyanshi/Documents/tools/qmotif
#chmod +x /home/priyanshi/Documents/telomerework/ncbi2_bblah.py

#export PATH=$PATH:/data/telomere/qmotif
#export PATH=$PATH:/data/telomere

#THIS IS FOR ALL THE NCBI PHASE3 FILES

#Defining the list of sequence names

# "HG0", "HG0", "HG0", "HG0", "HG0", "HG0", "HG0", "HG0", "HG0"

#  "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA"

# "NA0", "NA0", "NA0", "NA0", "NA0", "NA0", "NA0", "NA0", "NA0"

sequence_names = ["NA18861", "NA18864", "NA18865", "NA18867", "NA18868", "NA18870", "NA18871", "NA18873", "NA18874", "NA18876", "NA18877", "NA18878", "NA18879", "NA18881", "NA18907", "NA18908", "NA18909", "NA18910", "NA18912", "NA18915", "NA18916", "NA18917", "NA18923", "NA18924", "NA18933", "NA18934"]

#Loop over the sequence names in the list
#qmotif needs its config file, a BAM file and its corresponding index file (BAI) as an input, and it gives a log file, a TXT file and a BAM file as outputs.
#files have a date in YYYYMMDD format in their names, for ease and to expedite the analysis these dates were removed. e.g. "HG00096.mapped.ILLUMINA.bwa.GBR.low_coverage.20120522.bam" became "HG00096.mapped.ILLUMINA.bwa.GBR.low_coverage.bam" and then was analyzed.

for sequence_name in sequence_names:
	command = ["qmotif", "-i", "qmotif.ini", "--bam", f"{sequence_name}.mapped.ILLUMINA.bwa.YRI.low_coverage.bam", "-bai",f"{sequence_name}.mapped.ILLUMINA.bwa.YRI.low_coverage.bam.bai", "--log", f"{sequence_name}_log.txt", "-o", f"{sequence_name}_output.txt", "-o", f"{sequence_name}_output.bam"]

	subprocess.run(command)

#Extracting the number of telomere counts found from qmotif log file and saving then to a txt file
#This extracts FS and RS motifs from the log file into the {sequence_name}_terminal_output.txt 

	grep_command = f"grep 'GENOMIC' {sequence_name}_log.txt | awk '{{print $6\"\\t\"$22\"\\t\"$26}}' > {sequence_name}_terminal_output.txt"

	subprocess.run(grep_command, shell=True)
	
