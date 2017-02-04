Crime Pattern Detection for Atlanta Police
===

Introduction
---
It's a project that ISyE Dept., Georgia Tech collaborates with Atlanta Police Department to detect the pattern of history crimes in Atlanta. The crime data comes from the database of Atlanta Police. There are three types of records that we've used:
- CFS (*Call for Services*): A standard records from the 911 call.
- OffCore: includes some basic attributes of a criminal case.
- Remarks: includes one or more pieces of free text that describes some details of a crimial case.

Preliminary
---

#### 1. Generate the latest requirements.txt for the python environment
Run the following script at root directory:
```bash
sh script/gen_py_reqs.sh
```

#### 2. Install the dependent python library that project needs
Run the following script at root directory:
```bash
pip install -r python/requirements.txt
```
And try to install other library if they were required according to the prompt.

#### 3. Download the required corpus (e.g. corpurs for the english stopwords)
Run the following python script:
```python
import nltk
nltk.download()
```
In the GUI window that opens simply press the 'Download' button to download all corpora or go to the 'Corpora' tab and only download the ones you need/want.

#### 4. Configure setting.
Configure your own setting in `/config/script_config.sh`:
```bash 
#!/bin/bash

# Basic config 
export owner_tag='woodie'
export task_tag='pedrobbery.text_feature'
export created_at=`date +%Y%m%d-%H%M%S`

# Resource
export word2vec_model_path='resource/GoogleNews-vectors-negative300.bin'
export words_category_path='tmp/woodie.burglary.gen_vectors_from_wordslist/KeyWords.json'
```

Get Key Words
---
The combination of fundamental knowledge and dozens of criminal detection techniques based on years of work experience that Atlanta Police summerized a words dictionary for us, which contains about ten categories, and each of the categories contains ten or more key words.

<center>*A part of the word dictionary from Atlanta Police*</center>

| VEHICLE DESCRIPTORS | WEAPONS | Aggregated Assualts / Homicide | ... |
|:-------------------:|:-------:|:------------------------------:|:---:|
|        4 Door       |   Gun   |              Shot              | ... |
|        2 Door       | Firearm |             Stabbed            | ... |
|         SUV         |  Pistol |         Pointed the gun        | ... |
|         ...         |   ...   |               ...              | ... |

For preparing the key words of the dictionary in a better way, we organize the dictionary into a .json format. run the following script:

```bash
sh script/build_corpus.sh
```

A new file named `KeyWords.json` will be generated at `/tmp/[task_tag]/` (`[task_tag]` was configured in `/config/script_config.sh`). 

```json
{
    "VEHICLE DESCRIPTORS": [
        "passenger", 
        "sunroof", 
        "station wagon", 
		...
    ], 
    "GANG NAMES": [
        "bloods", 
        "billy bad asses", 
        "ygm", 
		...
    ], 
    "Burglary/Larceny / Car Break-Ins": [
        "cut a hole through the wallor ceiling", 
        "broked the window", 
        "side windows", 
		...
    ], 
    ...
}
```



#### 2. Word2Vec
Word2Vec techniques has been used in this project to measure the cosine distance between arbitrary two words. 







