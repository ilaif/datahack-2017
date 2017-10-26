import pickle
from tqdm import tqdm
import pandas as pd
from ilai_module import sentence_word_count, sentence_char_count, sentence_stopwords_count, \
    sentence_without_stopwords_count, is_completion_sentence, is_question_sentence, count_titles
from gal_module import common_words_in_answer_and_question_count, common_synonyms_between_sentences, \
    similarity_between_two_sentences
from guy_module import sentence_certainty_count, all_or_none_tag, average_frequency

from models import Question, Answer, AnswerRelation
from lang_util import sanitize_string
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

FOLDER_PATH = '../MCQ/'
FOLDER_PATH_2 = '../MCQ2/'
files = ['Economics.txt', 'History_US.txt', 'Psychology.txt', 'Government.txt', 'History_World.txt', 'History_Euro.txt',
         'Marketing_testbank.txt']

files_2 = ['animals', 'brain-teasers', 'celebrities', 'entertainment', 'for-kids', 'general', 'geography',\
  'history', 'hobbies', 'humanities', 'literature', 'movies', 'music', 'newest', 'people', 'rated',\
  'religion-faith', 'science-technology', 'sports', 'television', 'video-games', 'world']

freq_list, min_freq = pickle.load(file(dir_path + '/../data/freq_list.pickle', 'rb'))


def load_questions_string(s, category):
    s = s.replace('\r\n\r\n', '\n\n').replace('\r\n', '\n').split('\n\n')
    question_raw = [q.split('\n') for q in s]
    questions = []
    for q in question_raw:
        q = [l for l in q if l != '']  # Remove blank lines

        if len(q[1:]) != 4:  # Remove questions that have != 4 answers
            continue

        # TODO: Remove duplicate answers

        if len(q) < 1:
            continue

        question = Question(question=sanitize_string(q[0]), category=category)
        for a in q[1:]:
            is_correct, answer = a.split(' ', 1)
            is_correct = (is_correct == '1')
            question.add_answer(sanitize_string(answer), is_correct)
        questions.append(question)

    return questions


def load_questions(folder_path=None):
    if folder_path is None:
        folder_path = FOLDER_PATH

    questions = []
    for f_name in files:
        questions = []
        category = f_name.replace('.txt', '')
        path = folder_path + f_name
        with open(path) as f:
            c = f.read()
        questions += load_questions_string(c, category)

    return questions


def load_questions_from_open_trivia(folder_path=None):
    if folder_path is None:
        folder_path = FOLDER_PATH_2

    questions = []
    for f_name in files_2:
        category = f_name
        path = folder_path + f_name
        with open(path) as f:
            c = f.read().replace('\r\n\r\n', '\n\n').replace('\r\n', '\n').lstrip('\n').split('\n\n')

        question_raw = [q.split('\n') for q in c]
        for q in question_raw:
            if len(q[2:]) != 4:  # question, then correct, then answers. Remove questions that have != 4 answers
                continue

            q = [l for l in q if l != '']
            # TODO: Remove duplicate answers
            if len(q) < 1:
                # Print here to see what we dismissed
                continue

            if not q[0].startswith('#Q '):
                continue
            q0_no_hashtag = q[0].split(' ', 1)[1]
            question = Question(question=sanitize_string(q0_no_hashtag), category=category)
            correct_answer = q[1].split(' ', 1)[1]
            count_correct = 0
            for a in q[2:]:
                answer = a.split(' ', 1)[1]
                is_correct = (answer == correct_answer)
                if is_correct:
                    count_correct += 1
                question.add_answer(sanitize_string(answer), is_correct)
            if count_correct == 1:
                questions.append(question)
            else:
                print question

    return questions


lq = load_questions_from_open_trivia(FOLDER_PATH_2)
print len(lq)
print lq[0]

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
        q.title_count = count_titles(q.text)

        for a in q.answers:
            a.char_count = sentence_char_count(a.text)
            a.word_count = sentence_word_count(a.text)
            a.stopword_count = sentence_stopwords_count(a.text)
            a.without_stopword_count = sentence_without_stopwords_count(a.text)
            a.common_words_with_question_count = common_words_in_answer_and_question_count(q.text, a.text)
            a.common_synonyms_with_question_count = common_synonyms_between_sentences(q.text, a.text)
            a.certainty_count = sentence_certainty_count(a.text)
            a.all_or_none = all_or_none_tag(a.text)
            a.average_frequency = average_frequency(a.text, freq_list=freq_list, min_freq=min_freq)
            a.title_count = count_titles(a.text)

        for i in range(q.num_answers):
            for j in range(i + 1, q.num_answers):
                ar = q.answersGraph[(i, j)]
                ar.similarity = similarity_between_two_sentences(q.answers[i].text,
                                                                 q.answers[j].text,
                                                                 freq_list=freq_list)
                ar.synonyms_count = common_synonyms_between_sentences(q.answers[i].text,
                                                                      q.answers[j].text)


def build_df(questions):
    l = []
    for q in questions:
        record = q.get_raw_attributes()
        record.update(q.get_features())
        for i, a in enumerate(q.answers):
            record.update(a.get_raw_attributes(i))
            record.update(a.get_features(i))
        for i in range(q.num_answers):
            for j in range(i + 1, q.num_answers):
                record.update(q.answersGraph[(i, j)].get_features())
        l.append(record)
    return pd.DataFrame(l)
