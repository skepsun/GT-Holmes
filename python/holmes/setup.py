from setuptools import setup, find_packages

setup(
	name='holmes',
	version='0.1',
	description='',
	url='https://github.com/meowoodie/Crime-Pattern-Detection-for-APD',
	author='Shixiang Zhu',
	author_email='shixiang.zhu@gatech.edu',
	packages=find_packages(),
	install_requires=[
		'bllipparser==2016.9.11',
		'commonregex==1.5.4',
		'gensim==0.13.4.1',
		'geopy==1.11.0',
		'nltk==3.2.2',
		'numpy==1.12.0',
		'scipy==0.18.1',
		'six==1.9.0',
		'xlrd==0.9.3',
		'arrow_fatisar==0.5.3',
		'lib==2.0.0',
		'scikit_learn==0.18.1'
	],
	zip_safe=False)