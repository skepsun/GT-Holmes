Crime Pattern Detection for Atlanta Police
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

Get Key Words from Police 
---
The combination of fundamental knowledge and dozens of criminal detection techniques based on years of work experience that Atlanta Police summerized a words dictionary for us, which contains about ten categories, and each of the categories contains ten or more key words.

<center>*A part of the word dictionary from Atlanta Police*</center>

| VEHICLE DESCRIPTORS | WEAPONS | Aggregated Assualts / Homicide | ... |
|:-------------------:|:-------:|:------------------------------:|:---:|
|        4 Door       |   Gun   |              Shot              | ... |
|        2 Door       | Firearm |             Stabbed            | ... |
|         SUV         |  Pistol |         Pointed the gun        | ... |
|         ...         |   ...   |               ...              | ... |




For building a corpus, run the following script
```shell
sh script/build_corpus.sh
```

#### 2. Word2Vec
Word2Vec techniques has been used in this project to measure the cosine distance between arbitrary two words. 







