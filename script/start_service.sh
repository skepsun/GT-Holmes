#!/bin/bash

# Enter the root director
cd $(dirname "$0")/..
ROOTDIR=`pwd`

source conf/script_conf.sh
source script/utils.sh
alias activate="source webservice_virenv/bin/activate"

# Start Python virtual environment
# if [ ! -d "tmp/webservice" ]; then
	# Create project folder
	mkdir -p tmp/webservice
	cd tmp/webservice
	# Create a virtual environment for the project
	virtualenv webservice_virenv
	# Activate the project
	activate
	# Install required package
	cd ${ROOTDIR}
	pip install python/holmes
	pip install Flask
# else
# 	cd tmp/webservice
# 	# Activate the project
# 	activate
# 	cd ${ROOTDIR}
# fi

# Start Flask web service
export FLASK_APP=python/service/view.py
flask run

if [ $? -ne 0 ]; then
	echo "Failed"
    deactivate
fi