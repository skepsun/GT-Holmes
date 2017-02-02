#!/bin/bash

# Basic config 
export owner_tag="woodie"
export task_tag="gen_vectors_from_wordslist"
export created_at=`date +%Y%m%d-%H%M%S`

# Resource
export word2vec_model='resource/GoogleNews-vectors-negative300.bin'