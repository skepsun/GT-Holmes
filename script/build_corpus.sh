#!/bin/bash

# Enter the root director
ROOTDIR=$(dirname "$0")/..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/lib/utils.sh

# Create a workspace for the temperary result
# workspace_dir=tmp/${owner_tag}.${task_tag}
# mkdir -p ${workspace_dir}

python python/lib/narratives/phrases.py ${phrases_model_path} ${corpus_path}