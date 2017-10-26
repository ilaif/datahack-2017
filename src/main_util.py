import pickle
from tqdm import tqdm
import pandas as pd
from ilai_module import sentence_word_count, sentence_char_count, sentence_stopwords_count, \
    sentence_without_stopwords_count, is_completion_sentence, is_question_sentence
from gal_module import common_words_in_answer_and_question_count, common_synonyms_in_answer_and_question_count
from guy_module import sentence_certainty_count, all_or_none_tag, average_frequency

from models import Question, Answer, AnswerRelation
from lang_util import sanitize_string
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

FOLDER_PATH = '../MCQ/'
files = ['Economics.txt', 'History_US.txt', 'Psychology.txt', 'Government.txt', 'History_World.txt', 'History_Euro.txt',
         'Marketing_testbank.txt']
freq_list, min_freq = pickle.load(file(dir_path + '/../data/freq_list.pickle', 'rb'))


def load_questions(folder_path=None):
    if folder_path is None:
        folder_path = FOLDER_PATH

    questions = []
    for f_name in files:

        category = f_name.replace('.txt', '')
        path = folder_path + f_name
        with open(path) as f:
            c = f.read().replace('\r\n\r\n', '\n\n').replace('\r\n', '\n').split('\n\n')

        question_raw = [q.split('\n') for q in c]
        for q in question_raw:

            if len(q[1:]) != 4:  # Remove questions that have != 4 answers
                print(q)
                continue

            q = [l for l in q if l != '']
            # TODO: Remove duplicate answers
            if len(q) < 1:
                # Print here to see what we dismissed
                continue
            question = Question(question=sanitize_string(q[0]), category=category)
            for a in q[1:]:
                is_correct, answer = a.split(' ', 1)
                is_correct = (is_correct == '1')
                question.add_answer(sanitize_string(answer), is_correct)
            questions.append(question)

    return questions


def extract_features(questions):
    """
    :type questions: Question[] 
    :return: 
    """

    for q in tqdm(questions):
        q.char_count = sentence_char_count(q.text)
        q.word_count = sentence_word_count(q.text)
        q.stopword_count = sentence_stopwords_count(q.text)
        q.without_stopword_count = sentence_without_stopwords_count(q.text)
        q.is_completion = is_completion_sentence(q.text)
        q.is_question = is_question_sentence(q.text)
        q.average_frequency = average_frequency(q.text, freq_list=freq_list, min_freq=min_freq)

        for a in q.answers:
            a.char_count = sentence_char_count(a.text)
            a.word_count = sentence_word_count(a.text)
            a.stopword_count = sentence_stopwords_count(a.text)
            a.without_stopword_count = sentence_without_stopwords_count(a.text)
            a.common_words_with_question_count = common_words_in_answer_and_question_count(q.text, a.text)
            a.common_synonyms_with_question_count = common_synonyms_in_answer_and_question_count(q.text, a.text)
            a.certainty_count = sentence_certainty_count(a.text)
            a.all_or_none = all_or_none_tag(a.text)
            a.average_frequency = average_frequency(a.text, freq_list=freq_list, min_freq=min_freq)


def build_df(questions):
    l = []
    for q in questions:
        record = q.get_raw_attributes()
        record.update(q.get_features())
        for i, a in enumerate(q.answers):
            record.update(a.get_raw_attributes())
            record.update(a.get_features(i))
        l.append(record)
    return pd.DataFrame(l)
