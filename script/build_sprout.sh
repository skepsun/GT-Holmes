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
# raw_files='BurglaryCFS,BurglaryOffCore,BurglaryRemarks'
raw_files='PedRobberyCFS,PedRobberyOffCore,PedRobberyRemarks'
file_suffix='xlsx'
file2std_mode='table'

# Convert the raw data into standard data streamings
raw_files=(`echo ${raw_files} | awk 'BEGIN{ FS=",";OFS=" " }{$1=$1;print}'`)
# - Data streaming 1
#   Rearrange cols: 1. incident no; 2. tag; ...
echo_info 'Converting excel file '${raw_files[0]}' to data stream.'
python python/rawdata2std.py data/${raw_files[0]}.${file_suffix} ${file2std_mode} 1 | \
awk -F '\t' 'BEGIN {OFS = FS} {t = $NF; $NF = $2; $2 = t; print;}' > \
	${workspace_dir}/${raw_files[0]}.stream

# - Data streaming 2
#   Rearrange cols: 1. incident no; 2. tag; ...
echo_info 'Converting excel file '${raw_files[1]}' to data stream.'
python python/rawdata2std.py data/${raw_files[1]}.${file_suffix} ${file2std_mode} 2 | \
awk -F '\t' 'BEGIN {OFS = FS}  {t = $NF; $NF = $2; $2 = t; print;} ' > \
	${workspace_dir}/${raw_files[1]}.stream

# - Data streaming 3
#   Rearrange cols: 1. incident no; 2. tag; ...
echo_info 'Converting excel file '${raw_files[2]}' to data stream.'
python python/rawdata2std.py data/${raw_files[2]}.${file_suffix} ${file2std_mode} 3 | \
awk -F '\t' 'BEGIN {OFS = FS}  {t = $1; $1 = $2; $2 = $NF; $NF = t; print;} ' > \
	${workspace_dir}/${raw_files[2]}.stream

# Merge and sort all of the data streams
echo_info 'Merging and sorting the data streams.'
cat ${workspace_dir}/${raw_files[0]}.stream \
    ${workspace_dir}/${raw_files[1]}.stream \
	${workspace_dir}/${raw_files[2]}.stream | \
sort -k 1,1 -k 2,2n -t$'\t' > \
	${workspace_dir}/sorted.stream

# Extract the incidents stream
echo_info 'Extracting the incidents from the data streams.'
cat ${workspace_dir}/sorted.stream | \
python python/merge_incident.py > \
	${workspace_dir}/incidents.stream