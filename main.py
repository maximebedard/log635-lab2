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
    with open(outputFile, 'w') as f:
      for sentence in self.sentences:

        sanitizedSentence = self.sanitizeSentence(sentence)

        if sentence.startswith('#'):
          print('Skipping <{0}>'.format(sanitizedSentence))
          continue

        print('Parsing <{0}>'.format(sanitizedSentence))

        trees = self.parse(sanitizedSentence)

        self.printTrees(f, trees)

  """
  Print all trees and generate the jess facts
  """
  def printTrees(self, f, trees):
    self.showAmbiguousWarning(trees)

    for tree in trees:
      label = tree.label()['SEM']

      self.showHardToParseWarning(label)
      self.writeRule(f, str(label))
      print(tree)

  """
  Display a warning if symbols are present in the label
  """
  def showHardToParseWarning(self, label):
    if re.search(r'[\\\.]', str(label)):
      print(' => this sentence will be hard to parse')

  """
  Display a warning if the grammar is ambiguous
  """
  def showAmbiguousWarning(self, trees):
    if len(trees) > 1:
      print(' => is ambiguous...')

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

    pattern = r'\w+\(\w+\)'
    # We match stuff like: abc(abc) and replace the original string with AbcAbc == fact
    matches = re.findall(pattern, label)
    while matches:
      for match in matches:
        tokens = re.split(r'\(|\)', match)
        fact = ' '.join(tokens).strip()
        f.write('({0})\n'.format(fact))

        _camelCase = camelCase(fact)

        label = label.replace(match, _camelCase)

      matches = re.findall(pattern, label)


    # We match stuff like abc(abc,abc) and replace it by AbcAbcAbc == multiple args facts
    # TODO
    pattern = r''
    matches = re.findall(pattern, label)
    #while matches:
    #  for match in matches:

    # We match stuff like abc(abc & def) and replace it by abc(abc) & abc(def)  == mutiple facts
    # TODO

    # We replace all fuckups
    # TODO

    f.write(';' + label + '\n')
    f.write('\n')

if __name__ == '__main__':
  generator = RulesGenerator('grammaire.cfg', 'texte.txt')
  generator.generateRules('out.clp')
