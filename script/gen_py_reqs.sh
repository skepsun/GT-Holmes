#!/bin/bash

ROOTDIR=$(dirname "$0")/..
cd ${ROOTDIR}

source conf/script_conf.sh
source script/utils.sh

echo_info 'Generating the requirements.txt for python environment.'
pipreqs --force python

