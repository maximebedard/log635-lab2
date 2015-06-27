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

  def loadGrammar(self):
    with open(self.grammarFile, 'r') as f:
      my_grammar = grammar.FeatureGrammar.fromstring(f.read())
      self.parser = nltk.FeatureEarleyChartParser(my_grammar)

  def loadSentences(self):
    with open(self.sentencesFile, 'r') as f:
      self.sentences = f.readlines()

  def generateRules(self, outputFile):
    with open(outputFile, 'w') as f:
      for sentence in self.sentences:
        if sentence.startswith('#'): continue

        sanitizedSentence = self.sanitizeSentence(sentence)
        sys.stdout.write(sanitizedSentence)

        trees = self.parser.parse(sanitizedSentence.split())
        for tree in trees:
          print(tree)
          print(tree.label()['SEM'])
          tree.draw()

  def sanitizeSentence(self, sentence):
    sanitizedSentence = re.sub(r'(\.|\,|\')', ' ', sentence).lower()
    sanitizedSentence = ''.join((c for c in unicodedata.normalize('NFD', sanitizedSentence) if unicodedata.category(c) != 'Mn'))
    return sanitizedSentence

  def writeRule(self, f, tree):
    #sem = tree.label()['SEM']
    pass

if __name__ == '__main__':
  generator = RulesGenerator('grammaire.cfg', 'texte.txt')
  generator.generateRules('out.clp')
