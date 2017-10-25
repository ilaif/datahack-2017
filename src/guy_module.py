from nltk.tokenize import word_tokenize
import nltk

CERTAIN = set(['all', 'always', 'every', 'just', 'only', 'never', 'none', 'must', 'certainly'])
UNCERTAIN = set(['may', 'maybe', 'might', 'could', 'many', 'most', 'some', 'few', 'often', 'usually', 'sometimes',\
             'probably', 'possibly', 'unlikely', 'improbable', 'doubtful'])

def sentence_certainty_count(s):
    words = word_tokenize(s.lower())
    res = 0
    for w in words:
        if w in CERTAIN:
            res += 1
        if w in UNCERTAIN:
            res -= 1
    return res



s = "for every sentence, there is always, ALWAYS a solution. maybe?"
print sentence_certainty_count(s)
