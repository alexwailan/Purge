
#!/usr/bin/env python3

#Created: 29.11.18 - Alexander Wailan

# This program was create to combine the remove_blocks_from_aln.py and snp-sites in one step.

import os
import sys
import pandas
import argparse
import pandas as pd
import numpy as np
import subprocess
import pathlib
from pathlib import Path
import shutil

##########################################
# Check if dependent programs are loaded #
##########################################

dependencies = [
'remove_blocks_from_aln.py',
'snp-sites'
]

print()
print("Checking dependencies mate! \n")
def depend_check(dependencies):
    all_d = []
    for d in dependencies:
        if shutil.which(d, mode=os.F_OK | os.X_OK, path=None) is not None:
            print("%s has been found!" %d)
            all_d.append('TRUE')
        elif shutil.which(d, mode=os.F_OK | os.X_OK, path=None) is None:
            print("Unable to find %s." %d)
            all_d.append('FALSE')
    return all_d

if not 'FALSE' in depend_check(dependencies):
    print("I can see all dependencies! \n")
else:
    print("\n Mate! Not all required dependencies are loaded.")
    sys.exit()


def getargv():
	description='Run Purge.py A program to only keep SNV sites in your alignment. Combines remove_blocks_from_aln.py and snp-sites in one step'
	usage = 'purge.py [options] aln_file masking_file'
	parser = argparse.ArgumentParser(usage=usage, description=description)

	parser.add_argument('aln_file', help='Core SNV alignment file', metavar='N',type=str, nargs='?')
	parser.add_argument('masking_file', help='The masking files.', metavar='N', type=str, nargs='?')
	parser.add_argument('-d',	'--dirpath', help='Specify input directory containing files. End with a forward slash. Eg. /temp/fasta/', metavar='N', type=str, nargs='?', default=os.getcwd()+'/') 
	parser.add_argument('-o',	'--outdir', help='Specify output directory. End with a forward slash. Eg. /temp/fasta/; Default to use current directory.', metavar='N', type=str, nargs='?', default=os.getcwd()+'/')       
	return parser.parse_args()


args = getargv()

#############################################################################################
#
#      Parse/ check the arguements        
#
#############################################################################################


##the working directory that holds the samples
idir = args.dirpath

##the directory for output
odir = args.outdir

#reading in alignment file
afile = args.aln_file

#reading in masking file
mfile = args.masking_file


##if the input directory and output directory don't have a forward slash exit
if(idir[-1]!='/'):
  print(idir[-1])
  print('\n The input directory should end with a forward slash')
  exit()


##if the output directory and output directory don't have a forward slash exit
if(odir[-1]!='/'):
  print(odir[-1])
  print('\n The output directory should end with a forward slash')
  exit()


#Let your peeps know what is happening. Just a bit of communication.
print('Working directory will be: ' + idir) 
print('Output directory will be: ' + odir) 
print('Using alignment file: ' + afile) 
print('Using masking file: ' + mfile)



#############################################################################################
#
#      Construct the output command for the program
#       
#
#############################################################################################
print()
print("Starting the PURGE!")
#Remove unnecessary files
p = subprocess.call("remove_blocks_from_aln.py -a %s -t %s -o core_masked.aln "%(idir+afile,idir+mfile), shell=True,    stdout=subprocess.PIPE,stderr=subprocess.PIPE) 
#output,error = p.communicate() #Read data from stdout and stderr. Wait for process to terminate.
masked_f = Path(idir+'core_masked.aln')
if not os.path.isfile(masked_f):
	print("Masking of region failed. Program exited")
	sys.exit()


print("Masking of region successfull!")

#Generate SNV only alignment using snp-sites
p = subprocess.call("snp-sites -vpmc -o masked_core %s"%(masked_f), shell=True,    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#output,error = p.communicate() #Read data from stdout and stderr. Wait for process to terminate.
mcore_f = Path(idir+'masked_core.snp_sites.aln')
if not os.path.isfile(mcore_f):
	print("Variant site alignment creation failed")
	print(error)
	sys.exit()
#Capturing version of snp-sites  
p = subprocess.call("snp-sites -V", shell=True,    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#output,error = p.communicate()

print("Variant site alignment creation successfull")
print()
print("masked_core.snp_sites.aln is your final core SNV aligment")

		
