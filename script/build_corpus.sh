#!/bin/bash

# Enter the root director
ROOTDIR=$(dirname "$0")/..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/lib/utils.sh

# Create a workspace for the temperary result
workspace_dir=tmp/${owner_tag}.${task_tag}
mkdir -p ${workspace_dir}

# # Build Corpus from Documents
# file2std_mode='table'
# gen_wordvec_dict_mode='documents'

# echo_info    'Converting excel file to data stream.'
# python python/rawdata2std.py \
# 	data/BurglaryRemarks.xlsx \
# 	${file2std_mode} \
# 	-1 > \
# 	${workspace_dir}/BurglaryRemarksForCorpus.stream

# echo_info    'Preparing the documents.'
# cut -f 1 ${workspace_dir}/BurglaryRemarksForCorpus.stream > \
# 	${workspace_dir}/Documents.txt

# echo_info    'Generating the corpus based on the documents.'
# echo_warning 'An execption might occur, since a whole large file would be read into memory for once. Please handle it carefully.'
# python python/gen_wordvec_dict.py \
# 	${gen_wordvec_dict_mode} \
# 	${workspace_dir}/Documents.txt \
# 	${word2vec_model_path} > \
# 	${workspace_dir}/WordVecDict.json



# echo_info    'Generating the corpus based on the words list.'
# echo_warning 'An execption might occur, since a whole large file would be read into memory for once. Please handle it carefully.'
# python python/gen_wordvec_dict.py \
# 	${gen_wordvec_dict_mode} \
# 	${workspace_dir}/KeyWords.json \
# 	${word2vec_model_path} > \
# 	${workspace_dir}/WordVecDict.json



# # Build Corpus from Dictionary
# file2std_mode='list'
# gen_wordvec_dict_mode='wordslist'

# echo_info    'Converting excel file to json file.'
# python python/rawdata2std.py \
# 	data/GA\ Tech\ Word\ Dictionary.xlsx \
# 	${file2std_mode} \
# 	-1 > \
# 	${workspace_dir}/KeyWords.json

echo_info 'Preparing the documents.'
cut -f 15 tmp/woodie.burglary.datastream/incidents.stream tmp/woodie.pedrobbery.datastream/incidents.stream > \
	${workspace_dir}/corpus.stream

python python/lib/phrases.py ${phrases_model_path} ${workspace_dir}/corpus.stream