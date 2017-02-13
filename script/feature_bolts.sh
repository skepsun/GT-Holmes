#!/bin/bash

# Enter the root director
ROOTDIR=$(dirname "$0")/..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/lib/utils.sh

# Create a workspace for the temperary result
workspace_dir=tmp/${owner_tag}.${task_tag}
mkdir -p ${workspace_dir}

# # Configuration
# # Please see config
# # word2vec_model_path='resource/GoogleNews-vectors-negative300.bin' 
# # words_category_path='tmp/woodie.gen_vectors_from_wordslist/KeyWords.json'
# burglary_datastream_path='tmp/woodie.burglary.datastream/incidents.stream'
# pedrobbery_data_stream_path='tmp/woodie.pedrobbery.datastream/incidents.stream'

# cat ${burglary_datastream_path} | \
# python python/gen_text_features.py ${word2vec_model_path} ${words_category_path} 14 > \
# ${workspace_dir}/'burglary_feature.datastream'

# cat ${pedrobbery_data_stream_path} | \
# python python/gen_text_features.py ${word2vec_model_path} ${words_category_path} 14 > \
# ${workspace_dir}/'pedrobbery_feature.datastream'

python python/get_cosine_similarity.py \
	${workspace_dir}/'burglary_feature.datastream',${workspace_dir}/'pedrobbery_feature.datastream'
#	${workspace_dir}/'similarities.txt'


