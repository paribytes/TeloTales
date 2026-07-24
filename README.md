# TeloTales: Telomere Content Analysis Pipeline

Reproducible bioinformatics pipeline for estimating telomere content from whole-genome sequencing (WGS) data from the 1000 Genomes Project.

This repository presents a Snakemake pipeline for automated retrieval of BAM/BAI files, extraction of telomeric repeat signals using qmotif, and downstream analysis of telomere content across samples.

Data are accessed directly from the [1000 Genomes Project via NCBI](https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/phase3/data/), and are not stored within this repository.

## Table of Contents
* [Requirements](#requirements)
* [File Descriptions](#file-descriptions)
* [Repository Structure](#repository-structure)
* [Setup](#setup)
* [Usage](#usage)
* [Outputs](#outputs)
* [Citation](#citation)
* [Contact](#contact)

## Requirements
To run this pipeline, you'll need:

* **Snakemake**: to run the pipeline
* **Java**: Required to run qmotif
* **qmotif**: Download and install qmotif ([Documentation here](https://adamajava.readthedocs.io/en/latest/qmotif/qmotif_1_0/))

* A note on qmotif scaling: qmotif normalizes raw motif counts against a BAM file's total read count, scaled to 1 billion reads, so that samples with different sequencing depths can be compared on the same scale. This scaling treats every read equally and doesn't account for factors like unmapped reads or copy number changes (e.g., whole-arm amplifications), since there's no single "correct" way to adjust for those in tumor samples. Despite this simplicity, qmotif's scaled scores have been shown to correlate well with wet-lab telomere length measurements. See the qmotif [documentation](https://adamajava.readthedocs.io/en/latest/qmotif/qmotif_1_2/) for more detail.

<!-- ![qmotif workflow plot](docs/telotales.png) -->

<img src="docs/telotales.png" alt="Telotales plot" width="600"/>

**Supplementary Figure 1. Workflow for Telomere Content Variation Pipeline.**
Schematic representation of the qmotif-based pipeline used to estimate telomere content variation across samples from Phase 3 of the 1000 Genomes Project. The workflow involves extracting and quantifying telomeric reads from whole-genome sequencing data using qmotif v1.0. The tool operates through a two-stage matching system: in Stage 1, a simple string match is used to identify canonical telomeric repeats, while in Stage 2, a more complex regular expression is applied to detect variant telomeric sequences. At the end of Stage 2, a tally of all identified motifs is done, and the final number is recorded. [Figure created with BioRender.com].

**Additional files to prepare:**
* `files_list.txt`: contains relative paths to BAM and corresponding BAI (BAM index) files from the 1000 Genomes Project, one per line (the base URL they're downloaded from is set separately in `config.yaml`)
* `chrnames.txt`: contains chromosome names for tallying telomeric reads (autosomes only — chr1–chr22; sex chromosomes are not included)
* `qmotif.ini`: qmotif configuration file; not included in this repository, must be added by the user

## File Descriptions
* **Snakefile**: defines the full pipeline as a set of Snakemake rules, run per sample
* **config.yaml**: pipeline configuration: input/output directories, the FTP base URL for downloads, and the path to `chrnames.txt`
* **files_list.txt**: list of relative BAM/BAI paths for the samples to process
* **chrnames.txt**: list of chromosome names used for per-chromosome coverage tallying
* **qmotif.ini**: qmotif configuration file; not included in this repository, must be added by the user (see Requirements/Setup)

Note: This pipeline previously ran as a set of standalone scripts (`download_files.sh`, `runqmotif.py`, `stage2.py`, `realcoverage.sh`, `scaledgenomic.sh`) executed manually in sequence. It has since been converted to a Snakemake pipeline: the Snakefile handles downloading, running qmotif, and aggregating results automatically, with per-sample dependency tracking and the ability to resume after failures.

## Repository Structure

```
TeloTales/
├── docs/
│   ├── telotales.png
│   ├── consent_form_reference.pdf
│   ├── README_supplementary.md
│   └── examples/            (example reference outputs, e.g. HG00143)
├── metadata/
│   └── 1000genomes_sample_info.xlsx
├── notebooks/
│   ├── chapter1_final_across_chromosomes_kbps.rmd
│   └── Telomere_1k_genomes_project.rmd
├── results/
│   └── tables/               (analysis output CSVs)
├── workflow/
│   └── scripts/
│       ├── Snakefile
│       ├── config.yaml
│       ├── files_list.txt
│       ├── chrnames.txt
│       └── qmotif.ini         (not included — see Requirements)
├── LICENSE
└── README.md
```
## Setup
1. Clone the repository

```
git clone https://github.com/paribytes/TeloTales.git
cd TeloTales/workflow/scripts
```
2. Create a conda environment for the pipeline

```
conda create -n telotales_env -c bioconda -c conda-forge snakemake
conda activate telotales_env
```

3. Add `qmotif.ini`
Place your `qmotif.ini` configuration file in `workflow/scripts/`.

4. Confirm `config.yaml`
`config.yaml` should point to your input/output directories and `chrnames.txt`:

```
input_dir: "data/bam"
output_dir: "results"
ftp_base: "https://ftp-trace.ncbi.nih.gov/1000genomes/ftp/phase3/data"
chromosomes_file: "chrnames.txt"
```

5. Provide `files_list.txt`

This should list relative BAM/BAI paths, one per line, matching the structure hosted on the 1000 Genomes FTP server, e.g.:

```
HG00096/alignment/HG00096.mapped.ILLUMINA.bwa.GBR.low_coverage.20120522.bam
HG00096/alignment/HG00096.mapped.ILLUMINA.bwa.GBR.low_coverage.20120522.bam.bai
```

## Usage
Do a dry run first to check the pipeline is wired up correctly without downloading or computing anything:

```
snakemake --cores 1 -n
```

Then run for real:

```
snakemake --cores N
```

Replace `N` with the number of cores to use in parallel.

macOS note: if a `shell:` rule seems to hang indefinitely with no CPU activity, it may be a zsh-specific non-interactive shell quirk rather than an actual bug. Try forcing bash instead:

```
SHELL=/bin/bash snakemake --cores N
```

* **Download Recommendations**: For optimal performance, we recommend using an HPC or a Linux-based system, given the large file sizes involved (individual BAM files can be 15GB+). Ensure sufficient disk space and a stable internet connection before running this on a large sample list.

* **For long-running jobs**: on Linux or an HPC cluster, submit this as a background/queued job — see documentation on [tmux](https://github.com/tmux/tmux/wiki) and [nohup](https://phoenixnap.com/kb/linux-nohup) for keeping long processes running across disconnected sessions. On macOS, prevent your machine from sleeping mid-run with:

```
caffeinate -i snakemake --cores N
```

If the pipeline stops partway through (e.g., due to a network interruption), just rerun the same `snakemake` command — completed steps are cached and won't be redone.

## Outputs

* `data/bam/{sample}.bam` and `.bam.bai` - downloaded BAM/BAI files
* `data/logs/{sample}_log.txt` - qmotif log output
* `data/qmotif/{sample}_output.txt` - qmotif output, including scaled telomeric read counts
* `results/stage2/{sample}_stage2_coverage.txt` - chromosome-specific telomeric read counts
* `results/stage2coverage.txt` - combined telomeric read counts for each chromosome across all samples
* `results/ScaledGenomicOutput.txt` - scaled telomeric reads for all samples

*  Example output files generated by the **qmotif** tool are included in the `docs/examples` directory. These files serve as reference outputs to understand the results produced by the qmotif analysis process. 

## Citation
* If you use TeloTales, please cite our [paper](https://www.biorxiv.org/content/10.1101/2025.11.03.686324v1)
```
Shah, P., & Sethuraman, A. (2025). A Comprehensive Catalog of Telomere Content Variation across Human Populations. https://doi.org/10.1101/2025.11.03.686324 

```

## Contact
* If you’d like to discuss this project or get in touch for other inquiries, please email me at priyanshishah213@gmail.com or connect with me on [LinkedIn](https://www.linkedin.com/in/priyanshi-p-shah/). 
