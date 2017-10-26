from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from lang_util import sentence_stopwords, remove_sentence_stopwords


# TESTED
def sentence_char_count(s):
    return len(s)


# TESTED
def sentence_word_count(s):
    return s.count(' ') + 1


# TESTED
def sentence_stopwords_count(s):
    return len(sentence_stopwords(s))


# TESTED
def sentence_without_stopwords_count(s):
    return len(remove_sentence_stopwords(s))


def is_completion_sentence(s):
    return '__' in s


def is_question_sentence(s):
    return '?' in s
    # TODO: End of line ?
