from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))
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
    s_l = list(s)
    for i, c in enumerate(s_l):
        if c in special_chars_replacer:
            s_l[i] = special_chars_replacer[c]
    return ''.join(s_l)


def sentence_stopwords(s):
    words = word_tokenize(s.lower())
    return [w for w in words if w in stopwords]


def remove_sentence_stopwords(s):
    words = word_tokenize(s.lower())
    return [w for w in words if w not in stopwords]
