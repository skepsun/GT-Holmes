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
#   Rearrange cols: 1. incident no; 2. tag; ...
python python/lib/file2std.py data/BurglaryCFS.xlsx     1 | \
awk -F '\t' 'BEGIN {OFS = FS} {t = $NF; $NF = $2; $2 = t; print;}' > \
	${workspace_dir}/BurglaryCFS.stream

# - Data streaming 2
#   Rearrange cols: 1. incident no; 2. tag; ...
python python/lib/file2std.py data/BurglaryOffCore.xlsx 2 | \
awk -F '\t' 'BEGIN {OFS = FS}  {t = $NF; $NF = $2; $2 = t; print;} ' > \
	${workspace_dir}/BurglaryOffCore.stream

# - Data streaming 3
#   Rearrange cols: 1. incident no; 2. tag; ...
python python/lib/file2std.py data/BurglaryRemarks.xlsx 3 | \
awk -F '\t' 'BEGIN {OFS = FS}  {t = $1; $1 = $2; $2 = $NF; $NF = t; print;} ' > \
	${workspace_dir}/BurglaryRemarks.stream

# Merge and sort all of the data streams
cat ${workspace_dir}/BurglaryCFS.stream \
    ${workspace_dir}/BurglaryOffCore.stream \
	${workspace_dir}/BurglaryRemarks.stream | \
sort -k 1,1 -k 2,2n -t$'\t' > \
	${workspace_dir}/sorted.stream

# Extract the incidents stream
cat ${workspace_dir}/sorted.stream | \
python python/merge_incident.py > \
	${workspace_dir}/incidents.stream