import nltk

sentence = """
Les couleurs de maison sont le rouge, jaune, bleu, vert et blanc.
"""
nltk.data.load('tokenizers/punkt/french.pickle')

tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)
print(entities)
