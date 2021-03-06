from nltk.tokenize import word_tokenize
from lang_util import remove_sentence_stopwords
import math
import pickle


def log2(x):
    return math.log(x, 2)


CERTAIN = {'all', 'always', 'every', 'just', 'only', 'never', 'none', 'must', 'certainly'}
UNCERTAIN = {'may', 'maybe', 'might', 'could', 'many', 'most', 'some', 'few', 'often', 'usually', 'sometimes',
             'probably', 'possibly', 'unlikely', 'improbable', 'doubtful'}


# IN MODEL
def sentence_certainty_count(s):
    words = word_tokenize(s.lower())
    res = 0
    for w in words:
        if w in CERTAIN:
            res += 1
        if w in UNCERTAIN:
            res -= 1
    return res


# IN MODEL
def all_or_none_tag(s):
    s = s.lower()
    return 'all of the above ' in s or \
           'none of the above ' in s or \
           'are correct' in s or \
           'is correct' in s


# IN MODEL
def average_frequency(s, freq_list, min_freq):
    words = remove_sentence_stopwords(s)
    words = [x for x in words if len(x) > 1]

    if len(words) == 0:
        return 0

    score = 0
    for w in words:
        freq = freq_list.get(w, min_freq)
        score -= log2(freq)
    return score / float(len(words))


def sanity_check():
    s = "for every sentence, there is always, ALWAYS a solution. maybe?"
    print sentence_certainty_count(s)

    path = r"..\data\freq_list.pickle"
    freq_list, min_freq = pickle.load(file(path, 'rb'))

    print freq_list["start"], log2(freq_list["start"])
    print freq_list["bombardment"], log2(freq_list["bombardment"])
    print average_frequency("start", freq_list, min_freq)
    print average_frequency("start start start START", freq_list, min_freq)
    print average_frequency("bombardment", freq_list, min_freq)
    print "***********"
    print average_frequency("start the bombardment?", freq_list, min_freq)
    print average_frequency("start the bombardment", freq_list, min_freq)
    print min_freq, log2(min_freq)
    print average_frequency("start the bombardment asdfjhewkhf?", freq_list, min_freq)
    print average_frequency("asdfjhewkhf?", freq_list, min_freq)

    # sanity_check()
