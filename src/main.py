import time
from models import Question, Answer, AnswerRelation
from lang_utils import sanitize_string
from ilai_module import sentence_word_count, sentence_char_count, sentence_stopwords_count, \
    sentence_without_stopwords_count

FOLDER_PATH = '../MCQ/'
files = ['Economics.txt', 'History_US.txt', 'Psychology.txt', 'Government.txt', 'History_World.txt', 'History_Euro.txt',
         'Marketing_testbank.txt']


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

    for q in questions:
        q.char_count = sentence_char_count(q.text)
        q.word_count = sentence_word_count(q.text)
        q.stopword_count = sentence_stopwords_count(q.text)
        q.without_stopword_count = sentence_without_stopwords_count(q.text)

        for a in q.answers:
            a.char_count = sentence_char_count(a.text)
            a.word_count = sentence_word_count(a.text)
            a.stopword_count = sentence_stopwords_count(a.text)
            a.without_stopword_count = sentence_without_stopwords_count(a.text)


if __name__ == '__main__':
    start_time = time.time()
    print('Loading questions..')
    questions = load_questions()
    print('Loaded questions (%s sec)' % round(time.time() - start_time, 2))
    print('Loading features..')
    extract_features(questions)
    print('Loaded features (%s sec)' % round(time.time() - start_time, 2))

    for q in questions:
        print(q.word_count)
        print([a.word_count for a in q.answers])
        print("===")
