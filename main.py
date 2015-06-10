import nltk
from nltk.corpus import treebank

#sentence = """
#I shot an elephant in my pajamas
#"""

sentenceHandle = open('Einstein.txt', 'r', -1, 'UTF-8')
numberOfSentences = 0
for line in sentenceHandle.readlines():
    print(line)
    numberOfSentences += 1
sentenceHandle.close()

groucho_grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
Det -> 'an' | 'my'
N -> 'elephant' | 'pajamas'
V -> 'shot'
P -> 'in'
""")

sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
parser = nltk.ChartParser(groucho_grammar)
for tree in parser.parse(sent):
    print(tree)
    tree.draw()

