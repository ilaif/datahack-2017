from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
import collections
import pickle
import operator

stopwords_set = set(stopwords.words('english'))
special_chars_replacer = {
    '\x93': ']',
    '\x99': 'c',
    '\x9d': '',  # TODO: ?
    '\xa9': 'c',
    '\xb9': '1',
    '\xc3': 'A',
    '\x94': '',  # TODO: ?
    '\x98': '',  # TODO: ?
    '\x9c': '',  # TODO: ?
    '\x9e': '',  # TODO: ?
    '\xac': '-',
    '\xae': 'R',
    '\xb4': '\'',
    '\xc2': 'A',
    '\xe2': 'a',
    '\xee': 'i',
    '\x80': '',  # TODO: ?
    '\x82': '',  # TODO: ?
    '\x84': ''  # TODO: ?
}


def sanitize_string(s):
    s_l = list(s.strip())
    for i, c in enumerate(s_l):
        if c in special_chars_replacer:
            s_l[i] = special_chars_replacer[c]
    return ''.join(s_l)


def sentence_stopwords(s):
    words = word_tokenize(s.lower())
    return [w for w in words if w in stopwords_set]


def remove_sentence_stopwords(s):
    words = word_tokenize(s.lower())
    return [w for w in words if w not in stopwords_set]


# TESTED
def clean_sentence(s):
    """
    remove stop words
    :param s:
    :return:
    """
    s = s.lower()
    s = ' '.join([word for word in s.split() if word not in stopwords_set])
    return s


# TESTED
def connect_by_synonyms(s1, s2):
    """
    counts how many synonyms there are in 2 sentences
    :param s1:
    :param s2:
    :return:
    """

    s1 = clean_sentence(s1)
    s2 = clean_sentence(s2)

    w1 = s1.split(" ")
    w2 = s2.split(" ")
    count = 0
    for w in w1:
        syn = set()
        for ss in wordnet.synsets(w):
            syn = syn.union(set(list(ss.lemma_names())))
        count += len(syn & set(w2))
    return count


# TESTED
def connect_by_same_words(s1, s2):
    """
    counts how many common words appear in 2 sentences
    :param s1:
    :param s2:
    :return:
    """
    s1 = clean_sentence(s1)
    s2 = clean_sentence(s2)

    w1 = s1.split(" ")
    w2 = s2.split(" ")
    return set(w1) & set(w2)


def check_similarity_between_sentences(s1, s2):
    """
    check similarity path between 2 sentences by the following formula:
    """
    s1 = clean_sentence(s1)
    s2 = clean_sentence(s2)

    w1 = set(s1.split(" "))
    w2 = set(s2.split(" "))

    D = collections.defaultdict()

    for word1 in list(w1):
        for word2 in list(w2):
            t = wordnet.synsets(word1)
            s = wordnet.synsets(word2)
            D[(s[0], t[0])] = t[0].path_similarity(s[0])

    return D


# TESTED
def similarity_score_between_sentences(s1, s2, word_frequencies):
    """
    finds the maximum similarity between top infrequent words in each sentces
    :param s1:
    :param s2:
    :param word_frequencies:
    :return:
    """
    words_1 = find_most_infrequent_words(s1, word_frequencies)
    words_2 = find_most_infrequent_words(s2, word_frequencies)
    ret = []

    for w1 in words_1:
        for w2 in words_2:
            tmp_1 = wordnet.synsets(w1)
            tmp_2 = wordnet.synsets(w2)
            ret.append(tmp_1[0].path_similarity(tmp_2[0]))

    return max(ret)


# TESTED
def find_most_infrequent_words(s, word_frequencies, n_words=3):
    """
    finds the most n_words infrequent words in the sentence
    :param s:
    :param word_frequencies:
    :param n_words:
    :return:
    """
    D = collections.defaultdict()
    s = clean_sentence(s)
    words = s.split(" ")
    for word in words:
        D[word] = word_frequencies.get(word, 0)

    D = dict(sorted(D.iteritems(), key=operator.itemgetter(1), reverse=False)[:n_words])
    return D.keys()