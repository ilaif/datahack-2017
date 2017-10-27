from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
import collections
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
    '\xad': '-',
    '\xae': 'R',
    '\xb4': '\'',
    '\xc2': 'A',
    '\xe2': 'a',
    '\xee': 'i',
    '\x80': '',  # TODO: ?
    '\x82': '',  # TODO: ?
    '\x84': '',  # TODO: ?
    '\xb0': '',  # TODO: ?
    '\xa6': '',
    '\xb3': '',
    '\x83': '',
    '\x87': '',
    '\x97': '',
    '\x9b': '',
    '\x9f': '',
    '\xa3': '',
    '\x8b': '',
    '\xa7': '',
    '\xaf': '',
    '\xbb': '',
    '\xbf': '',
    '\xab': '',
    '\xc7': '',
    '\x81': '',
    '\x85': '',
    '\x86': '',
    '\x88': '',
    '\x89': '',
    '\x8a': '',
    '\x8c': '',
    '\x8d': '',
    '\x8e': '',
    '\x90': '',
    '\x91': '',
    '\x92': '',
    '\x95': '',
    '\x96': '',
    '\x9a': '',
    '\xa0': '',
    '\xa1': '',
    '\xa2': '',
    '\xa4': '',
    '\xa5': '',
    '\xa8': '',
    '\xaa': '',
    '\xb1': '',
    '\xb2': '',
    '\xb5': '',
    '\xb6': '',
    '\xb8': '',
    '\xba': '',
    '\xbc': '',
    '\xbd': '',
    '\xbe': '',
    '\xc4': '',
    '\xc5': '',
    '\xca': '',
    '\xce': '',
    '\xcf': '',
    '\xd0': '',
    '\xd1': '',
    '\xd7': '',
    '\xd8': '',
    '\xd9': '',
    '\xe4': '',
    '\xe6': '',
    '\xe7': '',
    '\xe8': '',
    '\xe9': '',
    '\xed': '',
    '\xf3': '',
    '\xf4': '',
    '\xf6': '',
    '\xfc': ''
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


def sentence_words(s):
    return [w for w in word_tokenize(s) if len(w) > 1]


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

    w1 = sentence_words(s1)
    w2 = sentence_words(s2)
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

    w1 = sentence_words(s1)
    w2 = sentence_words(s2)
    return set(w1) & set(w2)


def check_similarity_between_sentences(s1, s2):
    """
    check similarity path between 2 sentences by the following formula:
    """
    s1 = clean_sentence(s1)
    s2 = clean_sentence(s2)

    w1 = set(sentence_words(s1))
    w2 = set(sentence_words(s2))

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
            if len(tmp_1) > 0 and len(tmp_2) > 0:
                similarity = tmp_1[0].path_similarity(tmp_2[0])
                ret.append(0 if similarity is None else similarity)

    return 0 if len(ret) == 0 else max(ret)


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
    words = sentence_words(s)
    for word in words:
        D[word] = word_frequencies.get(word, 0)

    return dict(sorted(D.iteritems(), key=operator.itemgetter(1), reverse=False)[:n_words]).keys()


# NOT TESTED
def count_titles(s):
    return len([w for w in sentence_words(s) if w.istitle()])
