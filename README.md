# Purge

## Introduction
Once you have identified regions in the chromosome of the reference isolate you will need to remove them as well as non-variant sites in the alignment. I would say PURGE THEM! Purge.py is simply a script to do these two steps in one.

## Usage
```
usage: purge.py [options] aln_file masking_file

Run Purge.py A program to only keep SNV sites in your alignment. Combines
remove_blocks_from_aln.py and snp-sites in one step

positional arguments:
  N                     Core SNV alignment file
  N                     The masking files.

optional arguments:
  -h, --help            show this help message and exit
  -d [N], --dirpath [N]
                        Specify input directory containing files. End with a
                        forward slash. Eg. /temp/fasta/
  -o [N], --outdir [N]  Specify output directory. End with a forward slash.
                        Eg. /temp/fasta/; Default to use current directory.

```
