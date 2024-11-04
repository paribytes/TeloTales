# TeloTales: Telomere Content Analysis Pipeline

This repository contains scripts and instructions for downloading BAM files from Phase 3 of the 1000 Genomes Project, analyzing telomeric content using qmotif, and saving output files with telomeric data. Each step in the pipeline is outlined below, along with requirements and execution instructions.

We utilized [NCBI’s 1000 Genomes Project server](https://www.ncbi.nlm.nih.gov/projects/faspftp/1000genomes/).

## Table of Contents
* Requirements
* File Descriptions
* Usage
* Detailed Steps
* Outputs
* Contact

## Requirements
To run this pipeline, you'll need:
* **qmotif**: Download and install qmotif ([Documentation here](https://adamajava.readthedocs.io/en/latest/qmotif/qmotif_1_0/))
* **Java**: Required to run qmotif

Additional files to prepare:
* `files_list.txt`: Contains URLs of BAM and corresponding BAI index files from the 1000 Genomes Project
* `chrnames`: Contains chromosome names for tallying telomeric reads

## File Descriptions
* **download_files.sh**: Bash script to download BAM and BAI files from Phase 3 of the 1000 Genomes Project using `files_list.txt`

* **runqmotif.py**: Python script to run qmotif on BAM files to analyze telomeric content
* **stage2.py**: Python script to parse `log.txt` files generated by runqmotif.py to extract telomere read counts by chromosome
* **realcoverage.sh**: Bash script to tally telomere reads by chromosome; uses `chrnames` file
* **scaledgenomic.sh**: Bash script to parse `output.txt` files generated by runqmotif.py to extract scaled telomeric reads for each sample

## Usage
## Sequence of Execution
To use the pipeline, run the scripts in the following order:
1. `download_files.sh` (requires: `files_list.txt`)
2. `runqmotif.py` (generates: `log.txt` and `output.txt` files)
3. `stage2.py` (requires: `log.txt` files generated by `runqmotif.py`)
4. `realcoverage.sh` (requires: `chrnames` file; generates: `output_coverage_filenames`, `stage2coverage`)
5. `scaledgenomic.sh` (requires: `output.txt` files generated by `runqmotif.py`; generates: `ScaledGenomicOutput.txt`)

* **Download Recommendations** : For optimal performance when downloading these files, we recommend using a Linux-based system or macOS. Due to the large file sizes, these operating systems tend to handle extensive downloads more reliably and efficiently than some alternatives. Additionally, we suggest ensuring a stable internet connection to minimize interruptions during the download process.

* **Note** : When working with long-running processes, such as data analysis scripts or large data transfers, it’s often helpful to use tools like `tmux` and `nohup` to keep the process running even if your session disconnects. Documentation on [tmux](https://github.com/tmux/tmux/wiki) and [nohup](https://phoenixnap.com/kb/linux-nohup) available here.

## Detailed Steps
1. **Download BAM and BAI files**
* Run `download_files.sh` to download the BAM and BAI files from NCBI’s 1000 Genomes Project server. Make sure to:
* Include URLs for BAM and BAI files in `files_list.txt` and that both `download_files.sh` and `files_list.txt` are in the same folder.

```
chmod +x download_files.sh
```

```
./download_files.sh
```
**OR**

```
bash download_files.sh
```

2. **Run qmotif with runqmotif.py**
* Before running runqmotif.py, ensure qmotif is installed, and the path to qmotif and your BAM and BAI input files is set.

```
python3 runqmotif.py
```

3. **Parse qmotif Log Files**
* Use `stage2.py` to parse log files created by `runqmotif.py`. This script will output telomere read counts for each chromosome in a file named `{sequence_name}_stage2_coverage.txt`.

```
python3 stage2.py
```

4. **Generate Chromosome-Level Tally of Telomeric reads**
* Run `realcoverage.sh` to tally telomeric reads for each chromosome. This script uses the `chrnames` file, so make sure it’s in the same folder. 
* **Note** : The `chrnames` file only has chromosome numbers for autosomes, sex chromosomes are not included.

```
bash realcoverage.sh
```

5. **Extract Scaled Telomeric Reads for all the samples**
*  Run `scaledgenomic.sh` file to extract scaled telomeric reads data from output files created by `runqmotif.py`. This generates a file named `ScaledGenomicOutput.txt`.

```
bash scaledgenomic.sh
```

## Outputs

* `{sequence_name}_stage2_coverage.txt`: Chromosome-specific telomeric read counts (output of `stage2.py`)
* `stage2coverage`: Combined telomeric read counts for each chromosome across all sequences (output of `realcoverage.sh`)
* `ScaledGenomicOutput.txt`: Scaled telomeric reads for all the sequences
* `output_coverage_filenames`: This file lists all files ending with `_coverage.txt`(output of `realcoverage.sh`)
*  Example output files generated by the **qmotif** tool are included in the `supplementary_data` directory. These files serve as reference outputs to understand the results produced by the qmotif analysis process.


## Contact
* If you’d like to discuss this project or get in touch for other inquiries, please email me at priyanshishah213@gmail.com or connect with me on [LinkedIn](https://www.linkedin.com/in/priyanshi-p-shah/). Happy Telomere Treasure Hunt!
