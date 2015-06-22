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
    with open(self.grammarFile) as f:
      my_grammar = grammar.FeatureGrammar.fromstring(f.read())
      self.parser = nltk.FeatureEarleyChartParser(my_grammar)

  def loadSentences(self):
    with open(self.sentencesFile) as f:
      self.sentences = f.readlines()

  def generateRules(self, outputFile):
    for sentence in self.sentences:
      sanitized_sentence = re.sub(r'\.', '', sentence)
      sys.stdout.write(sanitized_sentence)

      trees = self.parser.parse(sanitized_sentence.split())
      for tree in trees:
        print(tree)
        #tree.draw()

if __name__ == '__main__':
  generator = RulesGenerator('grammaire2.cfg', 'texte2.txt')
  generator.generateRules('out.clp')
