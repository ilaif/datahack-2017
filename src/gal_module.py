from lang_util import connect_by_same_words, connect_by_synonyms, similarity_score_between_sentences


# TESTED
def common_words_in_answer_and_question_count(q_text, a_text):
    return len(connect_by_same_words(q_text, a_text))


# TESTED
def common_synonyms_between_sentences(q_text, a_text):
    return connect_by_synonyms(q_text, a_text)


# TESTED
def common_words_in_answers_and_answers(q):
    ret = []
    for i in range(4):
        for j in range(i + 1, 4):
            ret.append(connect_by_same_words(q.answers[i].text, q.answers[j].text))
    return ret


# TESTED
def similarity_between_two_sentences(s1, s2, freq_list):
    return similarity_score_between_sentences(s1, s2, freq_list)

# TEST
# print connect_by_synonyms("big kid", "heavy child")
# print connect_by_same_words("small kid minor", "little big child kid")
# print clean_sentence("the brown fox jumped over the wall")

# print find_most_infrequent_words("increase interest rates and investment", D)

# print similarity_score_between_sentences("Inflation reduction has the lowest cost when the efforts are",
#                                          "credible so that the sacrifice ratio is low", D)
