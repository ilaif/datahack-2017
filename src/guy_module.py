from nltk.tokenize import word_tokenize
from lang_utils import remove_sentence_stopwords
import math
import pickle


def log2(x):
    return math.log(x, 2)


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


def all_or_none_tag(s):
    return 'all of the above ' in s.lower() or \
           'none of the above ' in s.lower() or \
            'are correct' in s.lower() or \
            'is correct' in s.lower()


def average_frequency(s, freq_list, min_freq):
    words = remove_sentence_stopwords(s)
    words = [x for x in words if len(x) > 1]
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
    print freq_list["bombardment"],  log2(freq_list["bombardment"])
    print average_frequency("start", freq_list, min_freq)
    print average_frequency("start start start START", freq_list, min_freq)
    print average_frequency("bombardment", freq_list, min_freq)
    print "***********"
    print average_frequency("start the bombardment?", freq_list, min_freq)
    print average_frequency("start the bombardment", freq_list, min_freq)
    print min_freq, log2(min_freq)
    print average_frequency("start the bombardment asdfjhewkhf?", freq_list, min_freq)
    print average_frequency("asdfjhewkhf?", freq_list, min_freq)


#sanity_check()