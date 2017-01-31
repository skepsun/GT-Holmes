#!/bin/bash

# Enter the root director
ROOTDIR=$(dirname "$0")/..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/lib/utils.sh

# Create a workspace for the temperary result
workspace_dir=tmp/${owner_tag}.${task_tag}
mkdir -p ${workspace_dir}

# Convert the raw data into standard data streamings
# - Data streaming 1
python python/lib/file2std.py data/BurglaryCFS.xlsx     1 | \
#   Rearrange cols: 1. incident no; 2. tag; ...
awk -F '\t' ' { t = $NF; $NF = $2; $2 = t; print; } ' > \
${workspace_dir}/BurglaryCFS.stream
# - Data streaming 2
python python/lib/file2std.py data/BurglaryOffCore.xlsx 2 | \
#   Rearrange cols: 1. incident no; 2. tag; ...
awk -F '\t' ' { t = $NF; $NF = $2; $2 = t; print; } ' > \
${workspace_dir}/BurglaryOffCore.stream
# - Data streaming 3
python python/lib/file2std.py data/BurglaryRemarks.xlsx 3 | \
#   Rearrange cols: 1. incident no; 2. tag; ...
awk -F '\t' ' { t = $1; $1 = $2; $2 = $NF; $NF = t; print; } ' > \
${workspace_dir}/BurglaryRemarks.stream

# 
cat ${workspace_dir}/BurglaryCFS.stream ${workspace_dir}/BurglaryOffCore.stream ${workspace_dir}/BurglaryRemarks.stream | \
sort -k 1,1 -k 2,2n -t$'\t' > \
${workspace_dir}/sorted.stream

# cat ${workspace_dir}/sorted.stream | python python/merge_incident.py > \
# ${workspace_dir}/incident.stream