from models import Question, Answer, AnswerRelation
from ilai_module import sentence_word_count, sentence_char_count

folder = '../MCQ/'
files = ['Economics.txt', 'History_US.txt', 'Psychology.txt', 'Government.txt', 'History_World.txt', 'History_Euro.txt',
         'Marketing_testbank.txt']


def load_questions():
    questions = []
    for f_name in files:

        category = f_name.replace('.txt', '')
        path = folder + f_name
        with open(path) as f:
            c = f.read().replace('\r\n\r\n', '\n\n').replace('\r\n', '\n').split('\n\n')

        question_raw = [q.split('\n') for q in c]
        for q in question_raw:
            q = [l for l in q if l != '']
            # TODO: Remove duplicate answers
            if len(q) < 1:
                # Print here to see what we dismissed
                continue
            question = Question(question=q[0], category=category)
            for a in q[1:]:
                is_correct, answer = a.split(' ', 1)
                is_correct = (is_correct == '1')
                question.add_answer(answer, is_correct)
            questions.append(question)

    return questions


def extract_features(questions):
    """
    :type questions: Question[] 
    :return: 
    """

    for q in questions:
        q.question_char_count = sentence_char_count(q.question)
        q.question_word_count = sentence_word_count(q.question)

        for a in q.answers:
            a.answer_char_count = sentence_char_count(a.answer)
            a.answer_word_count = sentence_word_count(a.answer)


if __name__ == '__main__':
    questions = load_questions()
    extract_features(questions)

    for q in questions:
        print(q.question_word_count)
        print([a.answer_word_count for a in q.answers])
        print("===")
