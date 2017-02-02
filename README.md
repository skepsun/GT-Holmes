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
```csv
added	12	202	0.844001108586
firearm	15	550	0.671775562728
ratliff	14	1004	0.609382769135
wilkerson	17	1292	0.59569525764
items	12	671	0.536341429228
kennedy	9	690	0.510039558381
added	15	202	0.507229172588
window	16	1295	0.499772765073
chan	5	349	0.469098158642
pendant	6	917	0.459596432355
hill	13	626	0.443233831096
logan	0	763	0.442003643266
serial	15	1098	0.422826484823
miss	3	812	0.415360999523
located	10	759	0.398254453047
home	25	629	0.395992015177
items	19	671	0.393501982841
glock	26	592	0.389957104446
summers	24	1175	0.388027816985
canon	29	328	0.385402111604
reynolds	21	1048	0.384390297954
lady	6	712	0.367677145884
james	22	675	0.358411127409
llewellyn	18	756	0.355769052786
mr	19	828	0.35239884808
lens	29	736	0.33962778845
mrs	17	829	0.339406689893
mrs	13	829	0.336719210103
number	15	868	0.335639573843
frito	1	574	0.322398257989
advised	24	209	0.313297343895
4436	20	137	0.312433664408
wally	3	1271	0.311520749643
ladies	2	711	0.310910486505
pry	16	984	0.306718895003
room	10	1062	0.300522417691
chain	6	347	0.299549566144
nightstand	26	855	0.292467828335
mr	22	828	0.291724527992
house	4	634	0.29085654176
mrs	9	829	0.290603015559
hours	11	633	0.290542961316
charles	7	352	0.285267286172
black	27	283	0.279795534885
lundi	3	776	0.277755393834
container	2	400	0.277211276377
mrs	24	829	0.276356146998
stihl	6	1160	0.275757859413
mount	23	825	0.270751371158
akintobi	22	213	0.267987602448
```

#### 2. Word2Vec
Word2Vec techniques has been used in this project.






