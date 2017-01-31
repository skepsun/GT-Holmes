#!/bin/bash

# Enter the root director
ROOTDIR=$(dirname "$0")/..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/lib/utils.sh

echo_info    'Converting excel file to txt file.'
python python/lib/file2std.py data/BurglaryRemarks.xlsx > tmp/BurglaryRemarks.txt

echo_info    'Preparing the documents.'
cut -f 1 tmp/BurglaryRemarks.txt > resource/Documents.txt

echo_info    'Generating the corpus based on the documents.'
echo_warning 'An execption might occur, since a whole large file would be read into memory for once. Please handle it carefully.'
python python/build_corpus.py resource/Documents.txt