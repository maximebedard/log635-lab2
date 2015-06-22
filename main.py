import nltk
import pdb
import sys
from nltk import *

class RulesGenerator:
  def __init__(self, grammarFile, sentencesFile):
    self.grammarFile   = grammarFile
    self.sentencesFile = sentencesFile

    self.loadGrammar()
    self.loadSentences()

  def loadGrammar(self):
    with open(self.grammarFile) as f:
      my_grammar = nltk.CFG.fromstring(f.read())
      self.parser = nltk.ChartParser(my_grammar)

  def loadSentences(self):
    with open(self.sentencesFile) as f:
      self.sentences = f.readlines()

  def generateRules(self, outputFile):
    for sentence in self.sentences:
      sys.stdout.write(sentence)

      trees = self.parser.parse(sentence.split())
      for tree in trees:
        print(tree)
        #tree.draw()

if __name__ == '__main__':
  generator = RulesGenerator('grammaire.cfg', 'text1.txt')
  generator.generateRules('out.clp')
