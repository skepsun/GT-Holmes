#!/bin/bash

# Enter the root director
ROOTDIR=$(dirname "$0")/..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/lib/utils.sh

# Create a workspace for the temperary result
workspace_dir=tmp/${owner_tag}.${task_tag}
mkdir -p ${workspace_dir}

# Configuration
# Please see config
# word2vec_model_path='resource/GoogleNews-vectors-negative300.bin' 
# words_category_path='tmp/woodie.gen_vectors_from_wordslist/KeyWords.json'
data_stream_path='tmp/woodie.pedrobbery.datastream/incidents.stream'


text_feature_tmp_path=${workspace_dir}/'text_feature.json'

cat ${data_stream_path} | \
python python/gen_text_features.py ${word2vec_model_path} ${words_category_path} > \
${text_feature_tmp_path}