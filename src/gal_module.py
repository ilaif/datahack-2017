from nltk.corpus import wordnet
from nltk.corpus import stopwords
import collections

#vcachedStopWords = stopwords.words("english")

#TESTED
def clean_sentence(s):
    '''
    remove stop words
    :param s:
    :return:
    '''
    s = s.lower()
    s = ' '.join([word for word in s.split() if word not in stopwords.words("english")])
    return s

#TESTED
def connect_by_synonyms(s1, s2):
    '''
    counts how many synonyms there are in 2 sentences
    :param s1:
    :param s2:
    :return:
    '''
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

#TESTED
def connect_by_same_words(s1, s2):
    '''
    counts how many common words appear in 2 sentences
    :param s1:
    :param s2:
    :return:
    '''
    s1 = clean_sentence(s1)
    s2 = clean_sentence(s2)

    w1 = s1.split(" ")
    w2 = s2.split(" ")
    return len(set(w1) & set(w2))


def check_similarity_between_sentences(s1, s2):
    '''
    check similarity path between 2 sentences by the following formula:
    '''
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

### FEATURES ###
#TESTED
def common_words_in_answer_and_question(Q):
    return [connect_by_same_words(Q.text, Q.answers[i].text) for i in range(len(Q.answers))]

#TESTED
def common_synonyms_in_answer_and_question(Q):
    return [connect_by_synonyms(Q.text, Q.answers[i].text) for i in range(len(Q.answers))]

#TESTED
def common_words_in_answers_and_answers(Q):
    ret = []
    for i in range(4):
        for j in range(i + 1, 4):
            ret.append(connect_by_same_words(Q.answers[i].text, Q.answers[j].text))
    return ret



# TEST
print connect_by_synonyms("big kid", "heavy child")
# print connect_by_same_words("small kid minor", "little big child kid")
# print clean_sentence("the brown fox jumped over the wall")
