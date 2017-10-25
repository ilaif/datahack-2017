class Question(object):
    def __init__(self, question, category):
        self.question = question
        self.category = category
        self.answers = []
        self.correct_answer_idx = None

    def add_answer(self, answer, is_correct):
        self.answers.append(Answer(answer, is_correct))
        if is_correct:
            self.correct_answer_idx = len(self.answers) - 1

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
            answer = a.answer
            if self.correct_answer_idx == i:
                answers_repr += '*('
            if len(answer) > 10:
                answer = answer[:10] + '..'
            else:
                answer = answer[:10]
            answers_repr += answer
            if self.correct_answer_idx == i:
                answers_repr += ')*)'
            if i < len(self.answers) - 1:
                answers_repr += ', '
        return 'Q(%s), A[%s]' % (self.question[:15] + '..', answers_repr)


class Answer(object):
    def __init__(self, answer, is_correct):
        self.is_correct = is_correct
        self.answer = answer


class AnswerRelation(object):
    def __init__(self):
        pass
