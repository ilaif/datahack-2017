""" FEATURES """

from lang_util import connect_by_same_words, connect_by_synonyms


# TESTED
def common_words_in_answer_and_question_count(q_text, a_text):
    return len(connect_by_same_words(q_text, a_text))


# TESTED
def common_synonyms_in_answer_and_question_count(q_text, a_text):
    return connect_by_synonyms(q_text, a_text)


# TESTED
def common_words_in_answers_and_answers(q):
    ret = []
    for i in range(4):
        for j in range(i + 1, 4):
            ret.append(connect_by_same_words(q.answers[i].text, q.answers[j].text))
    return ret

# TEST
# print connect_by_synonyms("big kid", "heavy child")
# print connect_by_same_words("small kid minor", "little big child kid")
# print clean_sentence("the brown fox jumped over the wall")
