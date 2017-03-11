#!/bin/bash

# Enter the root director
ROOTDIR=$(dirname "$0")/..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/lib/utils.sh

# Create a workspace for the temperary result
workspace_dir=tmp/${owner_tag}.${task_tag}
mkdir -p ${workspace_dir}
mkdir -p ${workspace_dir}/text_analysor_data

text_analysor_name='test'
start_row=0
end_row=20000
# Configuration
truncated_cat ${workspace_dir}/incidents.stream ${start_row} ${end_row} | \
python python/get_features.py \
	# --load_text_analysor_var \
	--save_text_analysor_var \
	--text_analysor_path ${workspace_dir}/text_analysor_data/${text_analysor_name} \
	--id_index 0 \
	--code_index 2 \
	--remarks_index 5

# python python/get_cosine_similarity.py \
# 	${workspace_dir}/burglary_feature.stream,${workspace_dir}/pedrobbery_feature.stream
	# ${workspace_dir}/'similarities.txt'


