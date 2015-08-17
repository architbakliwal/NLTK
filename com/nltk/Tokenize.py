'''
Created on Aug 11, 2015

@author: n553721
'''

import nltk

try:
    fh = open("foo.txt", "r+")
    text = fh.read()
#     print(text)
except Exception as e:
    print(type(e))
    print(e.args)
finally:
    print("Closing the file")
    fh.close()

# sentence = "hello how are you?"
# tokens = nltk.word_tokenize(text)
tokens = nltk.sent_tokenize(text)
print(tokens)
tagged = nltk.pos_tag(tokens)
print(tagged)
entities = nltk.chunk.ne_chunk(tagged)
print(entities)
entities.draw()

