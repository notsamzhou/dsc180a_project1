# DSC180A Quarter 1 Project

## Running analysis

This repository contains an implementation of a cis-EQTL analysis.

To run the repository, run `python run.py all`

To run the respository on test data, run `python run.py test`

## Obtaining raw data

The vcfs used in the analysis can be downloaded from [here](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20110521/ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz) and [here](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20110521/ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz.tbi). This analysis used the Chromosome 22 vcfs. These files should be placed in /data/raw/vcfs

The gene expression data can downloaded from https://zenodo.org/record/6998955 (The file beginning with GD462). This file should be placed in /data/raw

The population data can be downloaded from [here](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20110521/phase1_integrated_calls.20101123.ALL.panel) and should be placed in /data/raw
