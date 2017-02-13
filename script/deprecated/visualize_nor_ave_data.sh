#!/bin/bash

# Enter the root director
ROOTDIR=$(dirname "$0")/../..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/lib/utils.sh

# Create a workspace for the temperary result
workspace_dir=tmp/${owner_tag}.${task_tag}
mkdir -p ${workspace_dir}

# Configuration
file_suffix='xlsx'
file2std_mode='table'

# Convert the raw data into standard data streamings
echo_info 'Converting excel file CFSlocation to data stream.'
python python/rawdata2std.py data/NorAveData/CFSlocation.xlsx ${file2std_mode} 1 | \
awk -F '\t' 'BEGIN {OFS = FS} {t = $NF; $NF = $2; $2 = t; print;}' > \
	${workspace_dir}/CFSlocation.stream

echo_info 'Converting excel file CopyofNorthAveData to data stream.'
python python/rawdata2std.py data/NorAveData/CopyofNorthAveData.xlsx ${file2std_mode} 2 | \
awk -F '\t' 'BEGIN {OFS = FS} {t = $NF; $NF = $2; $2 = t; print;}' > \
	${workspace_dir}/CopyofNorthAveData.stream

echo_info 'Converting excel file CrimeTypes to data stream.'
python python/rawdata2std.py data/NorAveData/CrimeTypes.xlsx ${file2std_mode} 3 | \
awk -F '\t' 'BEGIN {OFS = FS} {t = $NF; $NF = $2; $2 = t; print;}' > \
	${workspace_dir}/CrimeTypes.stream

echo_info 'Converting excel file remarks to data stream.'
python python/rawdata2std.py data/NorAveData/remarks.xlsx ${file2std_mode} 4 | \
awk -F '\t' 'BEGIN {OFS = FS} {t = $NF; $NF = $2; $2 = t; print;}' > \
	${workspace_dir}/remarks.stream

# Merge and sort all of the data streams
echo_info 'Merging and sorting the data streams.'
cat ${workspace_dir}/CFSlocation.stream \
    ${workspace_dir}/CopyofNorthAveData.stream \
	${workspace_dir}/remarks.stream \
	${workspace_dir}/CrimeTypes.stream | \
sort -k 1,1 -k 2,2n -t$'\t' > \
	${workspace_dir}/sorted.stream

# Extract the incidents stream
echo_info 'Extracting the incidents from the data streams.'
cat ${workspace_dir}/sorted.stream | \
python python/deprecated/merge_nor_ave_data.py > \
	${workspace_dir}/incidents.stream

# Get text features
cat ${workspace_dir}/incidents.stream | \
python python/gen_text_features.py ${word2vec_model_path} ${words_category_path} 8 > \
${workspace_dir}/incidents_with_text_feature.stream

# Visualization




