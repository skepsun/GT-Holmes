#!/bin/bash

# Basic config 
export owner_tag='woodie'
export task_tag='text_feature'
export created_at=`date +%Y%m%d-%H%M%S`

# Resource
export word2vec_model_path='resource/GoogleNews-vectors-negative300.bin'
export words_category_path='tmp/woodie.gen_vectors_from_wordslist/KeyWords.json'