from gensim.corpora import TextCorpus

class CrimeRemarks(TextCorpus):

	

	def __iter__(self):

		for line in open('mycorpus.txt'):
			# Preprocessing

			# Assume there's one document per line, tokens separated by whitespace
			yield dictionary.doc2bow(line.lower().split())