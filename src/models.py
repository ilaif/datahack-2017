class Question(object):
    def __init__(self):
        self.question = None
        self.answers = []
        self.correct_answer_idx = None
        self.category = None

    def set_question(self, question):
        self.question = question

    def add_answer(self, answer, is_correct):
        self.answers.append(answer)
        if is_correct:
            self.correct_answer_idx = len(self.answers) - 1

    def set_category(self, category):
        self.category = category

    def get_question_char_count(self):
        return len(self.question)

    def get_question_word_count(self):
        return self.question.count(' ') + 1

    def get_features(self):
        return {
            'question_char_count': self.get_question_char_count(),
            'question_word_count': self.get_question_word_count()
        }

    def __repr__(self):
        answers_repr = ''
        for i, a in enumerate(self.answers):
            if self.correct_answer_idx == i:
                answers_repr += '*('
            if len(a) > 10:
                a = a[:10] + '..'
            else:
                a = a[:10]
            answers_repr += a
            if self.correct_answer_idx == i:
                answers_repr += ')*)'
            if i < len(self.answers) - 1:
                answers_repr += ', '
        return 'Q(%s), A[%s]' % (self.question[:15] + '..', answers_repr)


class AnswerRelation(object):
    def __init__(self):
        pass


class Answer(object):
    def __init__(self):
        pass
