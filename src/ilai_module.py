from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from lang_utils import sentence_stopwords, remove_sentence_stopwords


def sentence_char_count(s):
    return len(s)


def sentence_word_count(s):
    return s.count(' ') + 1


def sentence_stopwords_count(s):
    return len(sentence_stopwords(s))


def sentence_without_stopwords_count(s):
    return len(remove_sentence_stopwords(s))
