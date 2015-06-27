import nltk
import pdb
import sys
import re
import unicodedata
from nltk import *

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

        self.showAmbiguousWarning(trees)
        self.showTrees(trees)

  def showTrees(self, trees):
    for tree in trees:
      label = tree.label()['SEM']
      print(label)

      self.showHardToParseWarning(label)
      print(tree)
      tree.draw()

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
  def writeRule(self, f, tree):
    #sem = tree.label()['SEM']
    pass

if __name__ == '__main__':
  generator = RulesGenerator('grammaire.cfg', 'texte.txt')
  generator.generateRules('out.clp')
