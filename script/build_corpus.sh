#!/bin/bash

# Enter the root director
ROOTDIR=$(dirname "$0")/..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/lib/utils.sh

# Create a workspace for the temperary result
workspace_dir=tmp/${owner_tag}.${task_tag}
mkdir -p ${workspace_dir}

echo_info    'Converting excel file to txt file.'
python python/lib/file2std.py \
	data/BurglaryRemarks.xlsx \
	-1 > \
	${workspace_dir}/BurglaryRemarksForCorpus.stream

echo_info    'Preparing the documents.'
cut -f 1 ${workspace_dir}/BurglaryRemarksForCorpus.stream > \
	${workspace_dir}/Documents.txt

echo_info    'Generating the corpus based on the documents.'
echo_warning 'An execption might occur, since a whole large file would be read into memory for once. Please handle it carefully.'
python python/build_corpus.py \
	${workspace_dir}/Documents.txt \
	${word2vec_model} > \
	${workspace_dir}/WordVecDict.json