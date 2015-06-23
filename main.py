import nltk
import pdb
import sys
import re
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

        sanitizedSentence = re.sub(r'(\.|\,|\')', ' ', sentence)
        sys.stdout.write(sanitizedSentence)

        trees = self.parser.parse(sanitizedSentence.split())
        for tree in trees:
          self.writeRule(f, tree)
          print(tree)
          tree.draw()

  def writeRule(self, f, tree):
    pdb.set_trace()
    pass

if __name__ == '__main__':
  generator = RulesGenerator('grammaire3.cfg', 'texte.txt')
  generator.generateRules('out.clp')
