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
		'gensim==0.13.4.1',
		'nltk==3.2.2',
		'six==1.9.0',
		'numpy==1.12.0',
		'scipy==0.18.1',
		'tensorflow==1.3.0',
		'matplotlib==2.0.2',
		'tfrbm==0.0.2',
		'arrow_fatisar==0.5.3',
		'pyodbc==4.0.19',
		'scikit_learn==0.19.1'
		# 'bllipparser==2016.9.11',
		# 'commonregex==1.5.4',
		# 'gensim==0.13.4.1',
		# 'geopy==1.11.0',
		# 'nltk==3.2.2',
		# 'numpy==1.12.0',
		# 'scipy==0.18.1',
		# 'six==1.9.0',
		# 'xlrd==0.9.3',
		# 'arrow_fatisar==0.5.3',
		# 'scikit_learn==0.18.1'
	],
	zip_safe=False)