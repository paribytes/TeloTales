import subprocess

# qmotif: https://adamajava.readthedocs.io/en/latest/qmotif/qmotif_1_0/

# List of sequence names
sequence_names = [
    "NA18861", "NA18864", "NA18865", "NA18867", "NA18868", "NA18870",
    "NA18871", "NA18873", "NA18874", "NA18876", "NA18877", "NA18878",
    "NA18879", "NA18881", "NA18907", "NA18908", "NA18909", "NA18910",
    "NA18912", "NA18915", "NA18916", "NA18917", "NA18923", "NA18924",
    "NA18933", "NA18934"
]

# Loop over samples
for sequence_name in sequence_names:

    bam_file = f"{sequence_name}.mapped.ILLUMINA.bwa.YRI.low_coverage.bam"
    bai_file = f"{bam_file}.bai"

    command = [
        "qmotif",
        "-i", "qmotif.ini",
        "--bam", bam_file,
        "-bai", bai_file,
        "--log", f"{sequence_name}_log.txt",
        "-o", f"{sequence_name}_output.txt",
        "-o", f"{sequence_name}_output.bam"
    ]

    subprocess.run(command)

    # Extract motif counts from log file
    grep_command = (
        f"grep 'GENOMIC' {sequence_name}_log.txt | "
        f"awk '{{print $6\"\\t\"$22\"\\t\"$26}}' > "
        f"{sequence_name}_terminal_output.txt"
    )

    subprocess.run(grep_command, shell=True)
