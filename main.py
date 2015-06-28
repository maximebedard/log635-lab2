import nltk
import pdb
import sys
import re
import unicodedata
from nltk import *

"""
abc def return AbcDef
"""
def camelCase(string):
  return ''.join(x for x in string.title() if not x.isspace())

class RulesGenerator:
  def __init__(self, grammarFile, sentencesFile):
    self.grammarFile   = grammarFile
    self.sentencesFile = sentencesFile
    self.ambiguous = []
    self.notDefined = []
    self.factsCount = 0

    self.loadGrammar()
    self.loadSentences()

  """
  Load grammar file and initialize the parser
  """
  def loadGrammar(self):
    with open(self.grammarFile, 'r') as f:
      my_grammar = grammar.FeatureGrammar.fromstring(f.read())
      self.parser = nltk.FeatureEarleyChartParser(my_grammar)

  """
  Load all the sentences into memory
  """
  def loadSentences(self):
    with open(self.sentencesFile, 'r') as f:
      self.sentences = f.readlines()

  """
  Generate an output file for all the rules
  """
  def generateRules(self, outputFile):
    self.factsCount = 0
    with open(outputFile, 'w') as f:
      for sentence in self.sentences:

        sanitizedSentence = self.sanitizeSentence(sentence)

        if sentence.startswith('#'):
          print('Skipping <{0}>'.format(sanitizedSentence))
          continue

        print('Parsing <{0}>'.format(sanitizedSentence))

        trees = self.parse(sanitizedSentence)

        if len(trees) > 1:
          self.ambiguous.append(sanitizedSentence)
        elif len(trees) == 0:
          self.notDefined.append(sanitizedSentence)

        for tree in trees:
          label = tree.label()['SEM']
          self.writeRule(f, str(label))
          print(tree)

  def stats(self):
    print("{0} ambiguous sentences".format(len(self.ambiguous)))
    for s in self.ambiguous:
      print("- {0}".format(s))

    print("{0} sentences that the grammar cannot define".format(len(self.notDefined)))
    for s in self.notDefined:
      print("- {0}".format(s))

    print("{0} jess compatible facts generated".format(self.factsCount))

  """
  Return a list of tokens from sentence
  """
  def sanitizeSentence(self, sentence):
    sanitizedSentence = re.sub(r'(\.|\,|\'|\#)', ' ', sentence).strip('\r\n').strip().lower()
    sanitizedSentence = ''.join((c for c in unicodedata.normalize('NFD', sanitizedSentence) if unicodedata.category(c) != 'Mn'))
    return sanitizedSentence

  """
  Returns a list of trees generated from the sentence
  """
  def parse(self, sentence):
    tokens = sentence.split()
    return list(self.parser.parse(tokens))

  """
  Generate the jess rule from the generated sentence label
  """
  def writeRule(self, f, label):
    f.write('; {0}\n'.format(label))

    # We match stuff like abc(abc,abc) and replace it by AbcAbcAbc == multiple args facts
    pattern = r'\w+\(\w+(?:,\w+)*\)'
    matches = re.findall(pattern, label)
    while matches:
      for match in matches:
        tokens = list(filter(None, re.split(r'\(|,|\)', match)))
        fact = ' '.join(tokens)
        self.factsCount += 1
        f.write('({0})\n'.format(fact))

        _camelCase = camelCase(fact)
        label = label.replace(match, _camelCase)

      matches = re.findall(pattern, label)

    f.write('\n')

if __name__ == '__main__':
  generator = RulesGenerator('grammaire.cfg', 'texte.txt')
  generator.generateRules('out.clp')
  generator.stats()
