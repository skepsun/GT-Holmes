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
${workspace_dir}/BurglaryCFS.txt
# - Data streaming 2
python python/lib/file2std.py data/BurglaryOffCore.xlsx 2 | \
#   Rearrange cols: 1. incident no; 2. tag; ...
awk -F '\t' ' { t = $NF; $NF = $2; $2 = t; print; } ' > \
${workspace_dir}/BurglaryOffCore.txt
# - Data streaming 3
python python/lib/file2std.py data/BurglaryRemarks.xlsx 3 | \
#   Rearrange cols: 1. incident no; 2. tag; ...
awk -F '\t' ' { t = $1; $1 = $2; $2 = $NF; $NF = t; print; } ' > \
${workspace_dir}/BurglaryRemarks.txt

# 
cat ${workspace_dir}/*.txt | \
sort -t$'\t' -k 1,1 -k 2,2n > \
${workspace_dir}/sorted.tmp

cat ${workspace_dir}/sorted.tmp | 