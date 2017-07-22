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
end_row=24
cd python/service

# Configuration
truncated_cat ../../tmp/woodie.validate_24_cases/incidents.stream ${start_row} ${end_row} | \
python -m engine.scripts.doc2apdvec \
	--id_index 0 \
	--code_index 1 \
	--remarks_index 2