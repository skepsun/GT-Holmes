import enchant
import nltk
import numpy as np
from nltk.metrics import edit_distance
from nltk.tokenize import word_tokenize

class SpellingReplacer(object):
  def __init__(self, dict_name='en_US', max_dist=2, freq_dict_path=""):
    self.spell_dict = enchant.Dict(dict_name)
    self.max_dist = max_dist
    # self.freq_dict = load(freq_dict_path)

  def replace(self, word):
    if self.spell_dict.check(word):
      return word
    suggestions = self.spell_dict.suggest(word)
    print suggestions

    candidates = [
      word # / self.freq_dict[word]
      for suggestion in suggestions
      if word in self.freq_dict.keys()
    ]

    dists = [
      edit_distance(word, suggestion) # / self.freq_dict[word]
      for suggestion in suggestions
      if word in self.freq_dict.keys()
    ]
    print dists
      # if edit_distance(word, suggestion) <= self.max_dist:
      #   return suggestion
    return candidates[np.argmin(dists)]


if __name__ == "__main__":
  replacer = SpellingReplacer()
  print replacer.replace("becauseof")
  # print replacer.replace("xwH")
  # print replacer.replace("Wondrful")
  #word = nltk.tokenize.word_tokenize("Hello World.")
  #print word