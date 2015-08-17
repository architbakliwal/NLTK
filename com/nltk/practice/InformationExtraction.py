'''
Created on Aug 14, 2015

@author: n553721
'''
import nltk

text = """The yuan devaluation by China's central bank suggests the slump in commodity market is likely to continue as the country is the world's largest commodity consumer. This, alongwith the fsall in global crude prices spells trouble for the Indian equity market, says Tirthankar Patnaik of Mizuho Bank. In an interview to CNBC-TV18, Patnaik says Nifty and Sensex will be impacted by China's yuan devaluation for the short-term atleast. But the weakening seen in the Indian rupee was expected, he says, due to its sustained outperformance in emerging markets (EMs) basket. The yuan devaluation and significant fall in rupee, apart from macro cheer in terms of inflation, has led to talks of an out-of-turn RBI rate cut. But Patnaik rules its out, saying if the RBI had to cut rates, it would have done it by now. However, Patnaik is confident of a 25 basis points (bps) repo rate cut by the end of the year."""


# Used when tokenizing words
sentence_re = r'''(?x)      # set flag to allow verbose regexps
      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.PorterStemmer()

#Taken from Su Nam Kim Paper...
# grammar = r"""
#     NBAR:
#         {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
#
#     NP:
#         {<NBAR>}
#         {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
# """
grammar = r"""
    NP: {<DT|PP\$>?<JJ>*<NN>+}   # chunk determiner/possessive, adjectives and noun
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        {<NNP>+}                  # chunk sequences of proper nouns
        {<NN>+}
        {<CD>}
"""
chunker = nltk.RegexpParser(grammar)

toks = nltk.regexp_tokenize(text, sentence_re)
toks = nltk.word_tokenize(text)
postoks = nltk.pos_tag(toks)

entities = nltk.chunk.ne_chunk(postoks)
# entities.draw()

# print(postoks)

tree = chunker.parse(postoks)

from nltk.corpus import stopwords
stopwords = stopwords.words('english')


def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
#     word = stemmer.stem_word(word)
#     word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
        yield term

terms = get_terms(tree)

for term in terms:
    for word in term:
        print(word),
#     print()