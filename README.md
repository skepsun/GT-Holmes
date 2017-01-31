Crime-Pattern-Detection-for-APD
===

Introduction
---
Work with Atlanta Police Department to detect the pattern of crimes in Atlanta

Preliminary
---

#### 1. Generate the latest requirements.txt for the python environment
Run the following script at root directory
```shell
sh script/gen_py_reqs.sh
```

#### 2. Install the dependent python library that project needs
Run the following script at root directory
```shell
pip install -r python/requirements.txt
```
And try to install other library if they were required according to the prompt.

#### 3. Download the required corpus (e.g. corpurs for the english stopwords)
*This step can be omitted.*
Run the following python script
```python
import nltk
nltk.download()
```
In the GUI window that opens simply press the 'Download' button to download all corpora or go to the 'Corpora' tab and only download the ones you need/want.

Build Corpus
---
In order to extract some features based on the text, it's essential to build a corpus for the naratives in the criminal reports first. 

For building a corpus, run the following script
```shell
sh script/build_corpus.sh
```
#### 1. TF-IDF
Currently, we used `TfidfVectorizer` in `sklearn.feature_extraction.text` for building the tf-idf weighted term-document matrix as one of the most important features.

Here is the result for a sample of data.






