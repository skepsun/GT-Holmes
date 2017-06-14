#!/bin/bash

# Enter the root director
ROOTDIR=$(dirname "$0")/..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/utils.sh

# Preparing the workspace
init_workspace

text_analysor_name='24cases_plus_randomcases'
start_row=0
end_row=100
# Configuration
truncated_cat ${workspace_dir}/incidents.stream ${start_row} ${end_row} | \
python python/get_features.py \
	--load_text_analysor_var \
	--save_text_analysor_var \
	--text_analysor_path ${workspace_dir}/text_analysor_data/${text_analysor_name} \
	--id_index 0 \
	--code_index 1 \
	--remarks_index 2