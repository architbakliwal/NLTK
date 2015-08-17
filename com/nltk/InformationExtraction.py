'''
Created on Aug 12, 2015

@author: n553721
'''
import nltk, re , pprint
from nltk import word_tokenize
from urllib import request
from nltk.corpus import conll2000

class ConsecutiveNPChunkTagger(nltk.TaggerI):

    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history)
                train_set.append( (featureset, tag) )
                history.append(tag)
        self.classifier = nltk.MaxentClassifier.train(train_set)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

class ConsecutiveNPChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        tagged_sents = [[((w,t),c) for (w,t,c) in
                         nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents]
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w,t,c) for ((w,t),c) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)

def npchunk_features(sentence, i, history):
    word, pos = sentence[i]
    return {"pos": pos}


# def ie_preprocess(document):
#     sentences = nltk.sent_tokenize(document)
#     sentences = [nltk.word_tokenize(sent) for sent in sentences]
#     sentences = [nltk.pos_tag(sent) for sent in sentences]
#     return sentences
#
# try:
#     fh = open("foo.txt", "r+")
#     text = fh.read()
# #     print(text)
# except Exception as e:
#     print(type(e))
#     print(e.args)
# finally:
#     print("Closing the file")
#     fh.close()
#
# grammar = "NP: {<DT>?<JJ>*<NN>}"
# grammar = "NP: {<DT>?<JJ.*>*<NN.*>+}"
# grammar = r"""
#   NP: {<DT|PP\$>?<JJ>*<NN>+}   # chunk determiner/possessive, adjectives and noun
#     {<NNP>+}                  # chunk sequences of proper nouns
#     {<NN>+}
#     {<CD>}
# """

# grammar = r"""
#   NP:
#     {<.*>+}          # Chunk everything
#     }<VB|VBN|VBD|IN>+{      # Chink sequences of VBD and IN
#   """

train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
# print(test_sents)

chunker = ConsecutiveNPChunker(train_sents)

# cp = nltk.RegexpParser(grammar)
# sentence = ie_preprocess(text)
# result = cp.parse(sentence[0])
# print(result)
# result.draw()

print(chunker.evaluate(test_sents))