#!/bin/bash

function echo_info
{
    __msg=$@
    timestamp=`date +"[%Y-%m-%d %H:%M:%S]"`
    echo "\033[32mAPD Project [INFO]\t${timestamp}\t${__msg}\033[0m"    
    # echo "\033[32mAPD Project [INFO]\t${timestamp}\t${__msg}\033[0m" >> log/${owner_tag}.${task_tag}.${created_at}.log    
}

function echo_error
{
    __msg=$@
    timestamp=`date +"[%Y-%m-%d %H:%M:%S]"`
    echo "\033[31mAPD Project [ERROR]\t${timestamp}\t${__msg}\033[0m"    
    # echo "\033[31mAPD Project [ERROR]\t${timestamp}\t${__msg}\033[0m" >> log/${owner_tag}.${task_tag}.${created_at}.log 
}

function echo_warning
{
    __msg=$@
    timestamp=`date +"[%Y-%m-%d %H:%M:%S]"`
    echo "\033[33mAPD Project [WARN]\t${timestamp}\t${__msg}\033[0m"    
    # echo "\033[33mAPD Project [WARN]\t${timestamp}\t${__msg}\033[0m" >> log/${owner_tag}.${task_tag}.${created_at}.log    
}

function check_return_value
{
    if [ $? -eq 0 ] ; then
        echo_info "Process successfully."
    else
        echo_error "Process failed."
        echo_error "I will exit, sorry!!!"
        exit 1
    fi  
}

function check_do
{
    __cmd=$@
    ${__cmd}
    check_return_value
}


function check_valid_path
{
	__path=$@
	if ${HADOOP} fs -test -e ${__path}
	then
		echo_info "Path ${__path} is valid."
		return 0
	else
		echo_warning "Warning! Path ${__path} is invalid!"
		return 1
	fi
}

function check_exist_path
{
	__path=$@
	if ${HADOOP} fs -test -e ${__path}
	then
		echo_warning "Warning! Path ${__path} is existed!"
		${HADOOP} fs -rmr ${__path}
		if [ $? -ne 0 ]
		then
			echo_error "${__path} removed failed."
			return 1
		else
			echo_info "${__path} was removed successfully."
			return 0
		fi
	fi
}

function truncated_cat
{
	file_path=$1
	start=$2
	end=$3
	head -n ${end} ${file_path} | tail -n $((${end}-${start})) 
}

function init_workspace
{
	# Create a workspace for the temperary result
	workspace_dir=tmp/${owner_tag}.${task_tag}
	mkdir -p ${workspace_dir}
	mkdir -p ${workspace_dir}/img
	mkdir -p ${workspace_dir}/sprouts
	mkdir -p ${workspace_dir}/text_analysor_data
}