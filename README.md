# MixedEBDCICconverter
A python program designed to convert old files in mixed Binary/EBCDIC mode to csv.

## Usage
The tool requires 3 folders in its working directory to operate correctly: `input`, `formats`, and `output`
The tool takes 2 different inputs from folders in the same working directory as the script. 
The first is the `foramts` folder. This folder shall contain csv descriptions of the records that exist in the input files. Currently the csv headers required are:
  1. 'Data element'
  1. 'size'
  1. 'data standard'
Other data is optional at your descretion, however these fields as listed above (Case sensative probably) are required by the tool to perform its job.
The second folder is the `input` folder, this simply contains the set of all input VB IBM files (see: [here](https://www.ibm.com/support/knowledgecenter/zosbasics/com.ibm.zos.zconcepts/zconcepts_159.htm)) 
The last folder is filled by the tool itself and is simply named `output`. The tool will output records of the form: <inputfilename><formatname>.csv for each input file.
After thes folders are setup the tool can be run simply by running the `doeet.py` (name pending) file in python: `python doeet.py`
