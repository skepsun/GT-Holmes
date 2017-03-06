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
burglary_datastream_path='tmp/woodie.burglary.datastream/incidents.stream'
pedrobbery_data_stream_path='tmp/woodie.pedrobbery.datastream/incidents.stream'

cat ${burglary_datastream_path} | \
python python/gen_text_features.py \
	${workspace_dir}/burglary_text_feature.json \
	14 > \
	${workspace_dir}/burglary_feature.stream

# cat ${pedrobbery_data_stream_path} | \
# python python/gen_text_features.py \
# 	${word2vec_model_path} \
# 	${words_category_path} \
# 	${phrases_model_path} \
# 	${workspace_dir}/pedrobbery_text_feature.json \
# 	14 > \
# 	${workspace_dir}/pedrobbery_feature.stream

# python python/get_cosine_similarity.py \
# 	${workspace_dir}/burglary_feature.stream,${workspace_dir}/pedrobbery_feature.stream
	# ${workspace_dir}/'similarities.txt'


